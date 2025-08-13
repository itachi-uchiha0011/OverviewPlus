from datetime import date, time
from ..extensions import db
from .base import BaseModel


class TodoItem(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(20), default="todo", nullable=False)  # todo | not_todo
    due_date = db.Column(db.Date)
    due_time = db.Column(db.Time)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    priority = db.Column(db.Integer, default=0, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))