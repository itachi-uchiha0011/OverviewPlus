from datetime import datetime, timedelta
from ..extensions import db
from .base import BaseModel


class PasswordResetToken(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)

    @staticmethod
    def create_for(user_id: int, ttl_minutes: int = 30) -> 'PasswordResetToken':
        import secrets
        t = PasswordResetToken(
            user_id=user_id,
            token=secrets.token_urlsafe(48),
            expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes),
        )
        db.session.add(t)
        db.session.commit()
        return t