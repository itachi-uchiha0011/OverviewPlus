from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Post, Like, Comment
from ..utils.sanitize import sanitize_html

posts_bp = Blueprint("posts", __name__)


@posts_bp.get("")
@jwt_required()
def list_posts():
    user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "content_html": p.content_html,
            "is_public": p.is_public,
            "slug": p.slug,
            "likes": len(p.likes),
            "comments": len(p.comments),
        }
        for p in posts
    ]


@posts_bp.post("")
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    body = request.get_json() or {}
    post = Post(
        user_id=user_id,
        title=body.get("title"),
        content_html=sanitize_html(body.get("content_html")),
        is_public=bool(body.get("is_public", False)),
        slug=body.get("slug"),
    )
    db.session.add(post)
    db.session.commit()
    return {"id": post.id}, 201


@posts_bp.put("/<int:post_id>")
@jwt_required()
def update_post(post_id: int):
    user_id = get_jwt_identity()
    post = Post.query.filter_by(id=post_id, user_id=user_id).first_or_404()
    body = request.get_json() or {}
    for field in ["title", "is_public", "slug"]:
        if field in body:
            setattr(post, field, body[field])
    if "content_html" in body:
        post.content_html = sanitize_html(body.get("content_html") or "")
    db.session.commit()
    return {"message": "Updated"}


@posts_bp.delete("/<int:post_id>")
@jwt_required()
def delete_post(post_id: int):
    user_id = get_jwt_identity()
    post = Post.query.filter_by(id=post_id, user_id=user_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return {"message": "Deleted"}


@posts_bp.get("/public")
def public_posts():
    posts = Post.query.filter_by(is_public=True).order_by(Post.created_at.desc()).limit(50).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "content_html": p.content_html,
            "slug": p.slug,
            "likes": len(p.likes),
            "comments": len(p.comments),
            "user_id": p.user_id,
        }
        for p in posts
    ]


@posts_bp.post("/<int:post_id>/like")
@jwt_required()
def like_post(post_id: int):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    if not post.is_public and post.user_id != user_id:
        return {"error": "Not allowed"}, 403

    existing = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if not existing:
        db.session.add(Like(user_id=user_id, post_id=post_id))
        db.session.commit()
    return {"message": "Liked"}


@posts_bp.delete("/<int:post_id>/like")
@jwt_required()
def unlike_post(post_id: int):
    user_id = get_jwt_identity()
    existing = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
    return {"message": "Unliked"}


@posts_bp.post("/<int:post_id>/comments")
@jwt_required()
def add_comment(post_id: int):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)
    if not post.is_public and post.user_id != user_id:
        return {"error": "Not allowed"}, 403

    body = request.get_json() or {}
    content = (body.get("content") or "").strip()
    if not content:
        return {"error": "Empty comment"}, 400
    db.session.add(Comment(user_id=user_id, post_id=post_id, content=content))
    db.session.commit()
    return {"message": "Comment added"}


@posts_bp.get("/<int:post_id>/comments")
def list_comments(post_id: int):
    post = Post.query.get_or_404(post_id)
    comments = (
        Comment.query.filter_by(post_id=post_id)
        .order_by(Comment.created_at.asc())
        .limit(200)
        .all()
    )
    return [
        {"id": c.id, "content": c.content, "user_id": c.user_id, "created_at": c.created_at.isoformat()}
        for c in comments
    ]