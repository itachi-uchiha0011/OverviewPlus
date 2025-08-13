from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import TodoItem


todos_bp = Blueprint("todos", __name__)


@todos_bp.get("")
@jwt_required()
def list_todos():
    user_id = get_jwt_identity()
    q = TodoItem.query.filter_by(user_id=user_id)
    if request.args.get("type"):
        q = q.filter_by(item_type=request.args.get("type"))
    todos = q.order_by(TodoItem.priority.desc()).limit(200).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "item_type": t.item_type,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "due_time": t.due_time.isoformat() if t.due_time else None,
            "completed": t.completed,
            "priority": t.priority,
            "category_id": t.category_id,
        }
        for t in todos
    ]


@todos_bp.post("")
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    body = request.get_json() or {}
    t = TodoItem(
        user_id=user_id,
        title=body.get("title"),
        item_type=body.get("item_type", "todo"),
        due_date=date.fromisoformat(body.get("due_date")) if body.get("due_date") else None,
        due_time=_parse_time(body.get("due_time")) if body.get("due_time") else None,
        completed=bool(body.get("completed", False)),
        priority=int(body.get("priority", 0)),
        category_id=body.get("category_id"),
    )
    db.session.add(t)
    db.session.commit()
    return {"id": t.id}, 201


@todos_bp.put("/<int:todo_id>")
@jwt_required()
def update_todo(todo_id: int):
    user_id = get_jwt_identity()
    t = TodoItem.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}

    for field in ["title", "item_type", "completed", "priority", "category_id"]:
        if field in body:
            setattr(t, field, body[field])
    if "due_date" in body:
        t.due_date = date.fromisoformat(body["due_date"]) if body["due_date"] else None
    if "due_time" in body:
        t.due_time = _parse_time(body["due_time"]) if body["due_time"] else None

    db.session.commit()
    return {"message": "Updated"}


@todos_bp.post("/<int:todo_id>/complete")
@jwt_required()
def complete(todo_id: int):
    user_id = get_jwt_identity()
    t = TodoItem.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    t.completed = True
    db.session.commit()
    return {"message": "Completed"}


@todos_bp.delete("/<int:todo_id>/complete")
@jwt_required()
def uncomplete(todo_id: int):
    user_id = get_jwt_identity()
    t = TodoItem.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    t.completed = False
    db.session.commit()
    return {"message": "Uncompleted"}


@todos_bp.delete("/<int:todo_id>")
@jwt_required()
def delete_todo(todo_id: int):
    user_id = get_jwt_identity()
    t = TodoItem.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    db.session.delete(t)
    db.session.commit()
    return {"message": "Deleted"}


def _parse_time(value: str):
    parts = value.split(":")
    if len(parts) < 2:
        raise ValueError("Invalid time")
    from datetime import time

    return time(hour=int(parts[0]), minute=int(parts[1]))