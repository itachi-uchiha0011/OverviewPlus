from datetime import date
from ..extensions import db
from .base import BaseModel


class HabitLog(BaseModel):
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    completed = db.Column(db.Boolean, default=True, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("habit_id", "date", name="uq_habitlog_habit_date"),
    )