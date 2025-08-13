from ..extensions import db
from .base import BaseModel


class Alert(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)

    schedule_type = db.Column(db.String(20), nullable=False)  # daily|weekly|monthly|cron
    schedule_data = db.Column(db.JSON)
    next_run_at = db.Column(db.DateTime)

    linked_type = db.Column(db.String(20))  # habit|todo
    linked_id = db.Column(db.Integer)

    notify_email = db.Column(db.Boolean, default=False, nullable=False)
    notify_telegram = db.Column(db.Boolean, default=False, nullable=False)
    notify_push = db.Column(db.Boolean, default=False, nullable=False)
    sound_enabled = db.Column(db.Boolean, default=True, nullable=False)