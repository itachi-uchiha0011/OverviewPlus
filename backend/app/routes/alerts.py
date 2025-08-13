from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Alert

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.get("")
@jwt_required()
def list_alerts():
    user_id = get_jwt_identity()
    alerts = Alert.query.filter_by(user_id=user_id).order_by(Alert.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "title": a.title,
            "schedule_type": a.schedule_type,
            "schedule_data": a.schedule_data,
            "notify_email": a.notify_email,
            "notify_telegram": a.notify_telegram,
            "notify_push": a.notify_push,
            "sound_enabled": a.sound_enabled,
            "linked_type": a.linked_type,
            "linked_id": a.linked_id,
        }
        for a in alerts
    ]


@alerts_bp.post("")
@jwt_required()
def create_alert():
    user_id = get_jwt_identity()
    body = request.get_json() or {}
    a = Alert(
        user_id=user_id,
        title=body.get("title"),
        schedule_type=body.get("schedule_type", "daily"),
        schedule_data=body.get("schedule_data"),
        notify_email=bool(body.get("notify_email", False)),
        notify_telegram=bool(body.get("notify_telegram", False)),
        notify_push=bool(body.get("notify_push", False)),
        sound_enabled=bool(body.get("sound_enabled", True)),
        linked_type=body.get("linked_type"),
        linked_id=body.get("linked_id"),
    )
    db.session.add(a)
    db.session.commit()
    return {"id": a.id}, 201


@alerts_bp.put("/<int:alert_id>")
@jwt_required()
def update_alert(alert_id: int):
    user_id = get_jwt_identity()
    a = Alert.query.filter_by(id=alert_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}
    for field in [
        "title",
        "schedule_type",
        "schedule_data",
        "notify_email",
        "notify_telegram",
        "notify_push",
        "sound_enabled",
        "linked_type",
        "linked_id",
    ]:
        if field in body:
            setattr(a, field, body[field])
    db.session.commit()
    return {"message": "Updated"}


@alerts_bp.delete("/<int:alert_id>")
@jwt_required()
def delete_alert(alert_id: int):
    user_id = get_jwt_identity()
    a = Alert.query.filter_by(id=alert_id, user_id=user_id).first_or_404()
    db.session.delete(a)
    db.session.commit()
    return {"message": "Deleted"}