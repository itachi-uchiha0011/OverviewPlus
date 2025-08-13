from ..extensions import db
from .base import BaseModel


class Page(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    title = db.Column(db.String(255), nullable=False)
    content_html = db.Column(db.Text)

    is_public = db.Column(db.Boolean, default=False, nullable=False)
    slug = db.Column(db.String(255), index=True)

    parent_page_id = db.Column(db.Integer, db.ForeignKey("page.id"))
    position = db.Column(db.Integer, default=0, nullable=False)

    parent_page = db.relationship("Page", remote_side="Page.id", backref="subpages")