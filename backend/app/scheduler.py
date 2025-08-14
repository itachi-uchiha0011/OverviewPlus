import threading
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from flask import current_app
from .extensions import db
from .models import Alert, User, NotificationSubscription
from .utils.emailer import send_email
from .utils.telegram import send_telegram_message
from .utils.push import send_web_push

_scheduler_started = False


def start_alert_scheduler(app):
    global _scheduler_started
    if _scheduler_started:
        return
    _scheduler_started = True

    def _runner():
        with app.app_context():
            while True:
                try:
                    _check_and_send()
                except Exception:
                    pass
                time.sleep(60)

    t = threading.Thread(target=_runner, daemon=True)
    t.start()


def _check_and_send():
    now_utc = datetime.utcnow()
    due = Alert.query.filter((Alert.next_run_at == None) | (Alert.next_run_at <= now_utc)).all()  # noqa: E711
    for alert in due:
        user = User.query.get(alert.user_id)
        if not user:
            continue
        # Check if should trigger right now per user's timezone
        if not _is_due_now(user.timezone, alert):
            # schedule next and skip
            alert.next_run_at = _compute_next_run(user.timezone, alert)
            db.session.commit()
            continue

        title = alert.title or (alert.linked_type or 'Reminder')
        body = f"Reminder: {title}"

        if alert.notify_email and user.notify_email_enabled and user.email:
            send_email(user.email, title, f"<p>{body}</p>")
        if alert.notify_telegram and user.notify_telegram_enabled and user.telegram_chat_id:
            send_telegram_message(user.telegram_chat_id, body)
        if alert.notify_push and user.notify_push_enabled:
            subs = NotificationSubscription.query.filter_by(user_id=user.id).all()
            for sub in subs:
                subscription = {
                    'endpoint': sub.endpoint,
                    'keys': {'p256dh': sub.p256dh, 'auth': sub.auth},
                }
                send_web_push(subscription, body)

        alert.next_run_at = _compute_next_run(user.timezone, alert)
        db.session.commit()


def _is_due_now(timezone_name: str, alert: Alert) -> bool:
    tz = ZoneInfo(timezone_name)
    now = datetime.now(tz)
    sched = alert.schedule_data or {}
    target_time = _parse_hm(sched.get('time')) if sched.get('time') else None

    if alert.schedule_type == 'daily':
        if target_time:
            return now.hour == target_time[0] and now.minute == target_time[1]
        return True
    if alert.schedule_type == 'weekly':
        weekday = int(sched.get('weekday', now.weekday()))
        if now.weekday() != weekday:
            return False
        if target_time:
            return now.hour == target_time[0] and now.minute == target_time[1]
        return True
    if alert.schedule_type == 'monthly':
        day = int(sched.get('day', now.day))
        if now.day != day:
            return False
        if target_time:
            return now.hour == target_time[0] and now.minute == target_time[1]
        return True
    # default
    return True


def _compute_next_run(timezone_name: str, alert: Alert) -> datetime:
    tz = ZoneInfo(timezone_name)
    now = datetime.now(tz)
    sched = alert.schedule_data or {}
    h, m = _parse_hm(sched.get('time')) if sched.get('time') else (now.hour, now.minute)

    if alert.schedule_type == 'daily':
        candidate = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if candidate <= now:
            candidate = candidate + timedelta(days=1)
        return candidate.astimezone(ZoneInfo('UTC'))
    if alert.schedule_type == 'weekly':
        weekday = int(sched.get('weekday', now.weekday()))
        days_ahead = (weekday - now.weekday()) % 7
        candidate = now.replace(hour=h, minute=m, second=0, microsecond=0) + timedelta(days=days_ahead)
        if candidate <= now:
            candidate += timedelta(days=7)
        return candidate.astimezone(ZoneInfo('UTC'))
    if alert.schedule_type == 'monthly':
        day = int(sched.get('day', min(now.day, 28)))
        month = now.month
        year = now.year
        # if already passed, go to next month
        candidate = now.replace(day=min(day, 28), hour=h, minute=m, second=0, microsecond=0)
        if candidate <= now:
            month += 1
            if month > 12:
                month = 1
                year += 1
        candidate = candidate.replace(year=year, month=month, day=min(day, 28))
        return candidate.astimezone(ZoneInfo('UTC'))
    return now.astimezone(ZoneInfo('UTC'))


def _parse_hm(value: str):
    parts = (value or '').split(':')
    return int(parts[0]), int(parts[1])