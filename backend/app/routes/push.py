from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import NotificationSubscription
from flask import current_app

push_bp = Blueprint("push", __name__)


@push_bp.get("/public-key")
def get_public_key():
    key = current_app.config.get("VAPID_PUBLIC_KEY")
    return {"publicKey": key}


@push_bp.post("/subscribe")
@jwt_required()
def subscribe():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    endpoint = data.get("endpoint")
    keys = data.get("keys") or {}
    p256dh = keys.get("p256dh")
    auth = keys.get("auth")
    if not endpoint or not p256dh or not auth:
        return {"error": "Invalid subscription"}, 400

    existing = NotificationSubscription.query.filter_by(user_id=user_id, endpoint=endpoint).first()
    if not existing:
        sub = NotificationSubscription(user_id=user_id, endpoint=endpoint, p256dh=p256dh, auth=auth)
        db.session.add(sub)
        db.session.commit()
    return {"message": "Subscribed"}


@push_bp.delete("/subscribe")
@jwt_required()
def unsubscribe():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    endpoint = data.get("endpoint")
    if not endpoint:
        return {"error": "endpoint required"}, 400
    sub = NotificationSubscription.query.filter_by(user_id=user_id, endpoint=endpoint).first()
    if sub:
        db.session.delete(sub)
        db.session.commit()
    return {"message": "Unsubscribed"}