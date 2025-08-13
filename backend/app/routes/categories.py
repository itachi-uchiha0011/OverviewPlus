from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Category

categories_bp = Blueprint("categories", __name__)


@categories_bp.get("")
@jwt_required()
def list_categories():
    user_id = get_jwt_identity()
    cats = Category.query.filter_by(user_id=user_id).order_by(Category.position.asc()).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "parent_id": c.parent_id,
            "is_public": c.is_public,
            "slug": c.slug,
            "position": c.position,
        }
        for c in cats
    ]


@categories_bp.post("")
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    body = request.get_json() or {}
    cat = Category(
        user_id=user_id,
        name=body.get("name"),
        description=body.get("description"),
        parent_id=body.get("parent_id"),
        is_public=bool(body.get("is_public", False)),
        slug=body.get("slug"),
        position=int(body.get("position", 0)),
    )
    db.session.add(cat)
    db.session.commit()
    return {"id": cat.id}, 201


@categories_bp.put("/<int:category_id>")
@jwt_required()
def update_category(category_id: int):
    user_id = get_jwt_identity()
    cat = Category.query.filter_by(id=category_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}

    for field in ["name", "description", "parent_id", "is_public", "slug", "position"]:
        if field in body:
            setattr(cat, field, body[field])

    db.session.commit()
    return {"message": "Updated"}


@categories_bp.delete("/<int:category_id>")
@jwt_required()
def delete_category(category_id: int):
    user_id = get_jwt_identity()
    cat = Category.query.filter_by(id=category_id, user_id=user_id).first_or_404()
    db.session.delete(cat)
    db.session.commit()
    return {"message": "Deleted"}


@categories_bp.get("/public/<int:user_id>")
def public_categories(user_id: int):
    cats = Category.query.filter_by(user_id=user_id, is_public=True).order_by(Category.position.asc()).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "parent_id": c.parent_id,
            "slug": c.slug,
            "position": c.position,
        }
        for c in cats
    ]