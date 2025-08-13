from ..extensions import db
from .base import BaseModel


class Post(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content_html = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    slug = db.Column(db.String(255), unique=True, index=True)

    likes = db.relationship("Like", backref="post", cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan")


class Like(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False, index=True)

    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="uq_like_user_post"),
    )


class Comment(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)