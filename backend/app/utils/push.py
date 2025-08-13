from pywebpush import webpush, WebPushException
from flask import current_app


def send_web_push(subscription: dict, payload: str) -> bool:
    public_key = current_app.config.get('VAPID_PUBLIC_KEY')
    private_key = current_app.config.get('VAPID_PRIVATE_KEY')
    email = current_app.config.get('VAPID_EMAIL')
    if not public_key or not private_key or not email:
        return False
    try:
        webpush(
            subscription_info=subscription,
            data=payload,
            vapid_private_key=private_key,
            vapid_claims={"sub": f"mailto:{email}"},
            vapid_public_key=public_key,
        )
        return True
    except WebPushException:
        return False