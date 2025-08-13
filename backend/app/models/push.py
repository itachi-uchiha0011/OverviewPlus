from ..extensions import db
from .base import BaseModel


class NotificationSubscription(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    endpoint = db.Column(db.String(1000), nullable=False)
    p256dh = db.Column(db.String(255), nullable=False)
    auth = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "endpoint", name="uq_push_user_endpoint"),
    )