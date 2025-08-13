from datetime import date
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Habit, HabitLog, TodoItem, JournalEntry


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("")
@jwt_required()
def get_dashboard():
    user_id = get_jwt_identity()
    today = date.today()

    habits = Habit.query.filter_by(user_id=user_id).all()
    today_logs = HabitLog.query.filter_by(date=today).all()
    completed_habit_ids = {lg.habit_id for lg in today_logs}

    todos = (
        TodoItem.query.filter_by(user_id=user_id, item_type="todo", completed=False)
        .order_by(TodoItem.priority.desc())
        .limit(4)
        .all()
    )
    not_todos = (
        TodoItem.query.filter_by(user_id=user_id, item_type="not_todo", completed=False)
        .order_by(TodoItem.priority.desc())
        .limit(4)
        .all()
    )

    entries_today = JournalEntry.query.filter_by(user_id=user_id, date=today).count()

    return {
        "today": today.isoformat(),
        "habits": [
            {"id": h.id, "name": h.name, "completed": h.id in completed_habit_ids}
            for h in habits
        ],
        "todos": [{"id": t.id, "title": t.title} for t in todos],
        "not_todos": [{"id": t.id, "title": t.title} for t in not_todos],
        "journal_entries_today": entries_today,
        "stats": {
            "streaks": None,
            "completion_percent": None,
        },
    }