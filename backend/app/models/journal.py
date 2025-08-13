from ..extensions import db
from .base import BaseModel

journal_entry_tags = db.Table(
    "journal_entry_tags",
    db.Column("entry_id", db.Integer, db.ForeignKey("journalentry.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("journaltag.id"), primary_key=True),
)


class JournalEntry(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    content_html = db.Column(db.Text, nullable=False)
    content_text = db.Column(db.Text)

    tags = db.relationship("JournalTag", secondary=journal_entry_tags, backref="entries")


class JournalTag(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    name = db.Column(db.String(64), nullable=False)
    __table_args__ = (
        db.UniqueConstraint("user_id", "name", name="uq_journaltag_user_name"),
    )