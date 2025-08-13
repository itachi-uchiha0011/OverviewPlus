from ..extensions import db
from .base import BaseModel


class Category(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    slug = db.Column(db.String(255), index=True)
    position = db.Column(db.Integer, default=0, nullable=False)

    parent = db.relationship("Category", remote_side="Category.id", backref="children")

    pages = db.relationship("Page", backref="category", cascade="all, delete-orphan")