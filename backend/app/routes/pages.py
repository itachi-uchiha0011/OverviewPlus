from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Page

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("")
@jwt_required()
def list_pages():
    user_id = get_jwt_identity()
    q = Page.query.filter_by(user_id=user_id)
    if request.args.get("category_id"):
        q = q.filter_by(category_id=int(request.args.get("category_id")))
    pages = q.order_by(Page.position.asc()).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "content_html": p.content_html,
            "is_public": p.is_public,
            "slug": p.slug,
            "category_id": p.category_id,
            "parent_page_id": p.parent_page_id,
            "position": p.position,
        }
        for p in pages
    ]


@pages_bp.post("")
@jwt_required()
def create_page():
    user_id = get_jwt_identity()
    body = request.get_json() or {}
    page = Page(
        user_id=user_id,
        category_id=body.get("category_id"),
        title=body.get("title"),
        content_html=body.get("content_html"),
        is_public=bool(body.get("is_public", False)),
        slug=body.get("slug"),
        parent_page_id=body.get("parent_page_id"),
        position=int(body.get("position", 0)),
    )
    db.session.add(page)
    db.session.commit()
    return {"id": page.id}, 201


@pages_bp.put("/<int:page_id>")
@jwt_required()
def update_page(page_id: int):
    user_id = get_jwt_identity()
    page = Page.query.filter_by(id=page_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}

    for field in [
        "title",
        "content_html",
        "is_public",
        "slug",
        "category_id",
        "parent_page_id",
        "position",
    ]:
        if field in body:
            setattr(page, field, body[field])

    db.session.commit()
    return {"message": "Updated"}


@pages_bp.delete("/<int:page_id>")
@jwt_required()
def delete_page(page_id: int):
    user_id = get_jwt_identity()
    page = Page.query.filter_by(id=page_id, user_id=user_id).first_or_404()
    db.session.delete(page)
    db.session.commit()
    return {"message": "Deleted"}


@pages_bp.get("/public/<int:user_id>")
def public_pages(user_id: int):
    q = Page.query.filter_by(user_id=user_id, is_public=True)
    if request.args.get("category_id"):
        q = q.filter_by(category_id=int(request.args.get("category_id")))
    pages = q.order_by(Page.position.asc()).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "content_html": p.content_html,
            "slug": p.slug,
            "category_id": p.category_id,
            "parent_page_id": p.parent_page_id,
        }
        for p in pages
    ]