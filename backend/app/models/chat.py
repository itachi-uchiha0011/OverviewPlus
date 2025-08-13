from ..extensions import db
from .base import BaseModel


class Channel(BaseModel):
    name = db.Column(db.String(120), nullable=False)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    members = db.relationship("ChannelMember", backref="channel", cascade="all, delete-orphan")
    messages = db.relationship("Message", backref="channel", cascade="all, delete-orphan")


class ChannelMember(BaseModel):
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    role = db.Column(db.String(20), default="member", nullable=False)  # member|admin

    __table_args__ = (
        db.UniqueConstraint("channel_id", "user_id", name="uq_channel_member"),
    )


class Message(BaseModel):
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    content = db.Column(db.Text)
    file_url = db.Column(db.String(1000))