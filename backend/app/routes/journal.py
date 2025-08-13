from datetime import date
from collections import defaultdict
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import JournalEntry, JournalTag

journal_bp = Blueprint("journal", __name__)


@journal_bp.get("")
@jwt_required()
def list_entries():
    user_id = get_jwt_identity()
    q = JournalEntry.query.filter_by(user_id=user_id)
    if request.args.get("from"):
        q = q.filter(JournalEntry.date >= date.fromisoformat(request.args["from"]))
    if request.args.get("to"):
        q = q.filter(JournalEntry.date <= date.fromisoformat(request.args["to"]))
    entries = q.order_by(JournalEntry.date.desc()).limit(200).all()
    return [
        {
            "id": e.id,
            "date": e.date.isoformat(),
            "content_html": e.content_html,
            "tags": [t.name for t in e.tags],
        }
        for e in entries
    ]


@journal_bp.post("")
@jwt_required()
def create_entry():
    user_id = get_jwt_identity()
    body = request.get_json() or {}
    entry = JournalEntry(
        user_id=user_id,
        date=date.fromisoformat(body.get("date")) if body.get("date") else date.today(),
        content_html=body.get("content_html", ""),
        content_text=body.get("content_text"),
    )
    tag_names = body.get("tags") or []
    entry.tags = _get_or_create_tags(user_id, tag_names)
    db.session.add(entry)
    db.session.commit()
    return {"id": entry.id}, 201


@journal_bp.put("/<int:entry_id>")
@jwt_required()
def update_entry(entry_id: int):
    user_id = get_jwt_identity()
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}

    if "date" in body:
        entry.date = date.fromisoformat(body["date"]) if body["date"] else entry.date
    if "content_html" in body:
        entry.content_html = body["content_html"]
    if "content_text" in body:
        entry.content_text = body["content_text"]
    if "tags" in body:
        entry.tags = _get_or_create_tags(user_id, body.get("tags") or [])

    db.session.commit()
    return {"message": "Updated"}


@journal_bp.delete("/<int:entry_id>")
@jwt_required()
def delete_entry(entry_id: int):
    user_id = get_jwt_identity()
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    return {"message": "Deleted"}


@journal_bp.get("/heatmap")
@jwt_required()
def heatmap():
    user_id = get_jwt_identity()
    q = JournalEntry.query.filter_by(user_id=user_id)
    if request.args.get("year"):
        year = int(request.args.get("year"))
        from datetime import date as _date

        q = q.filter(JournalEntry.date >= _date(year, 1, 1), JournalEntry.date <= _date(year, 12, 31))
    counts = defaultdict(int)
    for e in q.all():
        counts[e.date.isoformat()] += 1
    return counts


def _get_or_create_tags(user_id: int, names: list[str]):
    lower = [n.strip().lower() for n in names if n and n.strip()]
    if not lower:
        return []
    existing = JournalTag.query.filter(JournalTag.user_id == user_id, JournalTag.name.in_(lower)).all()
    existing_map = {t.name: t for t in existing}
    result = []
    for name in lower:
        if name in existing_map:
            result.append(existing_map[name])
        else:
            tag = JournalTag(user_id=user_id, name=name)
            db.session.add(tag)
            result.append(tag)
    return result