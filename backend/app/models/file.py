from ..extensions import db
from .base import BaseModel


class FileObject(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    page_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(1000), nullable=False)
    mime_type = db.Column(db.String(100))
    size_bytes = db.Column(db.Integer)
    is_public = db.Column(db.Boolean, default=False, nullable=False)