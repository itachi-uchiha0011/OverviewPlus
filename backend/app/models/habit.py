from datetime import date, time
from ..extensions import db
from .base import BaseModel


class Habit(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)

    frequency = db.Column(db.String(20), default="daily", nullable=False)  # daily/weekly/custom
    custom_days = db.Column(db.JSON)  # e.g., [1,3,5]

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    color = db.Column(db.String(20))
    icon = db.Column(db.String(50))

    reminder_time = db.Column(db.Time)  # optional daily reminder time

    logs = db.relationship("HabitLog", backref="habit", cascade="all, delete-orphan")