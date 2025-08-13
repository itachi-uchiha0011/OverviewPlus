from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import User

users_bp = Blueprint("users", __name__)


@users_bp.get("/me")
@jwt_required()
def me():
    user = User.query.get_or_404(get_jwt_identity())
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
        "is_public": user.is_public,
        "phone": user.phone,
        "notify_email_enabled": user.notify_email_enabled,
        "notify_telegram_enabled": user.notify_telegram_enabled,
        "notify_push_enabled": user.notify_push_enabled,
        "timezone": user.timezone,
        "theme": user.theme,
    }


@users_bp.put("/me")
@jwt_required()
def update_me():
    user = User.query.get_or_404(get_jwt_identity())
    data = request.get_json() or {}

    for field in [
        "display_name",
        "bio",
        "avatar_url",
        "is_public",
        "phone",
        "notify_email_enabled",
        "notify_telegram_enabled",
        "notify_push_enabled",
        "timezone",
        "theme",
    ]:
        if field in data:
            setattr(user, field, data[field])

    db.session.commit()
    return {"message": "Profile updated"}


@users_bp.get("/public/<int:user_id>")
def public_profile(user_id: int):
    user = User.query.get_or_404(user_id)
    if not user.is_public:
        return {"error": "Profile is private"}, 403
    return user.to_public_dict()