from datetime import datetime
from ..extensions import db
from .base import BaseModel


class User(BaseModel):
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    display_name = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(500))
    is_public = db.Column(db.Boolean, default=False, nullable=False)

    phone = db.Column(db.String(30))

    notify_email_enabled = db.Column(db.Boolean, default=True, nullable=False)
    notify_telegram_enabled = db.Column(db.Boolean, default=False, nullable=False)
    notify_push_enabled = db.Column(db.Boolean, default=False, nullable=False)

    timezone = db.Column(db.String(64), default="Asia/Kolkata", nullable=False)
    theme = db.Column(db.String(20), default="light", nullable=False)

    telegram_chat_id = db.Column(db.String(64))

    # Relationships
    habits = db.relationship("Habit", backref="user", cascade="all, delete-orphan")
    todos = db.relationship("TodoItem", backref="user", cascade="all, delete-orphan")
    journal_entries = db.relationship(
        "JournalEntry", backref="user", cascade="all, delete-orphan"
    )
    categories = db.relationship("Category", backref="user", cascade="all, delete-orphan")
    pages = db.relationship("Page", backref="user", cascade="all, delete-orphan")
    files = db.relationship("FileObject", backref="user", cascade="all, delete-orphan")
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    channels = db.relationship("Channel", backref="owner", cascade="all, delete-orphan")

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "display_name": self.display_name,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "is_public": self.is_public,
        }