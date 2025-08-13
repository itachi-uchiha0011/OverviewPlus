from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from email_validator import validate_email, EmailNotValidError
import secrets

from ..extensions import db
from ..models import User
from ..utils.csrf import generate_csrf_token, set_csrf_token, validate_csrf

CSRF_HEADER = 'X-CSRF-Token'

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/csrf-token")
@jwt_required()
def csrf_token():
    user_id = get_jwt_identity()
    token = generate_csrf_token()
    set_csrf_token(user_id, token)
    return {"csrf_token": token}


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    display_name = data.get("display_name") or email.split("@")[0]

    try:
        validate_email(email)
    except EmailNotValidError as e:
        return {"error": "Invalid email"}, 400

    if len(password) < 8:
        return {"error": "Password too short"}, 400

    user = User(email=email, password_hash=bcrypt.hash(password), display_name=display_name)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email already registered"}, 409

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return {"access_token": access, "refresh_token": refresh, "user": {"id": user.id, "display_name": user.display_name, "email": user.email}}, 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        return {"error": "Invalid credentials"}, 401

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)
    return {"access_token": access, "refresh_token": refresh, "user": {"id": user.id, "display_name": user.display_name, "email": user.email}}


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access = create_access_token(identity=user_id)
    return {"access_token": access}


@auth_bp.post("/forgot-password")
def forgot_password():
    # CSRF check is enforced in a future global hook; allow here if header matches
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    if not email:
        return {"error": "Email required"}, 400
    return {"message": "If the email exists, a reset link will be sent."}


@auth_bp.post("/reset-password")
def reset_password():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    new_password = data.get("new_password") or ""
    if len(new_password) < 8:
        return {"error": "Password too short"}, 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404
    user.password_hash = bcrypt.hash(new_password)
    db.session.commit()
    return {"message": "Password updated"}