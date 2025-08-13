from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Habit, HabitLog

habits_bp = Blueprint("habits", __name__)


@habits_bp.get("")
@jwt_required()
def list_habits():
    user_id = get_jwt_identity()
    habits = Habit.query.filter_by(user_id=user_id).order_by(Habit.created_at.desc()).all()
    return [
        {
            "id": h.id,
            "name": h.name,
            "frequency": h.frequency,
            "custom_days": h.custom_days,
            "category_id": h.category_id,
            "start_date": h.start_date.isoformat() if h.start_date else None,
            "end_date": h.end_date.isoformat() if h.end_date else None,
            "color": h.color,
            "icon": h.icon,
            "reminder_time": h.reminder_time.isoformat() if h.reminder_time else None,
        }
        for h in habits
    ]


@habits_bp.post("")
@jwt_required()
def create_habit():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    habit = Habit(
        user_id=user_id,
        name=data.get("name"),
        frequency=data.get("frequency", "daily"),
        custom_days=data.get("custom_days"),
        category_id=data.get("category_id"),
        start_date=date.fromisoformat(data["start_date"]) if data.get("start_date") else None,
        end_date=date.fromisoformat(data["end_date"]) if data.get("end_date") else None,
        color=data.get("color"),
        icon=data.get("icon"),
        reminder_time=None,
    )
    if data.get("reminder_time"):
        try:
            habit.reminder_time = _parse_time(data.get("reminder_time"))
        except ValueError:
            return {"error": "Invalid reminder_time"}, 400

    db.session.add(habit)
    db.session.commit()
    return {"id": habit.id}, 201


@habits_bp.put("/<int:habit_id>")
@jwt_required()
def update_habit(habit_id: int):
    user_id = get_jwt_identity()
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    data = request.get_json() or {}

    for field in ["name", "frequency", "custom_days", "category_id", "color", "icon"]:
        if field in data:
            setattr(habit, field, data[field])

    if "start_date" in data:
        habit.start_date = date.fromisoformat(data["start_date"]) if data["start_date"] else None
    if "end_date" in data:
        habit.end_date = date.fromisoformat(data["end_date"]) if data["end_date"] else None
    if "reminder_time" in data:
        habit.reminder_time = _parse_time(data["reminder_time"]) if data["reminder_time"] else None

    db.session.commit()
    return {"message": "Habit updated"}


@habits_bp.delete("/<int:habit_id>")
@jwt_required()
def delete_habit(habit_id: int):
    user_id = get_jwt_identity()
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    db.session.delete(habit)
    db.session.commit()
    return {"message": "Habit deleted"}


@habits_bp.get("/<int:habit_id>/logs")
@jwt_required()
def list_logs(habit_id: int):
    user_id = get_jwt_identity()
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    logs = HabitLog.query.filter_by(habit_id=habit.id).order_by(HabitLog.date.desc()).all()
    return [
        {"id": lg.id, "date": lg.date.isoformat(), "completed": lg.completed}
        for lg in logs
    ]


@habits_bp.post("/<int:habit_id>/complete")
@jwt_required()
def complete(habit_id: int):
    user_id = get_jwt_identity()
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}
    the_date = date.fromisoformat(body.get("date")) if body.get("date") else date.today()

    log = HabitLog.query.filter_by(habit_id=habit.id, date=the_date).first()
    if not log:
        log = HabitLog(habit_id=habit.id, date=the_date, completed=True)
        db.session.add(log)
    else:
        log.completed = True
    db.session.commit()
    return {"message": "Completed", "log_id": log.id}


@habits_bp.delete("/<int:habit_id>/complete")
@jwt_required()
def uncomplete(habit_id: int):
    user_id = get_jwt_identity()
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}
    the_date = date.fromisoformat(body.get("date")) if body.get("date") else date.today()

    log = HabitLog.query.filter_by(habit_id=habit.id, date=the_date).first()
    if log:
        db.session.delete(log)
        db.session.commit()
    return {"message": "Uncompleted"}


def _parse_time(value: str):
    parts = value.split(":")
    if len(parts) < 2:
        raise ValueError("Invalid time")
    from datetime import time

    return time(hour=int(parts[0]), minute=int(parts[1]))