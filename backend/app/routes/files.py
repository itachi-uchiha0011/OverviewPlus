import os
from uuid import uuid4
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models import FileObject
from ..utils.storage import upload_file

files_bp = Blueprint("files", __name__)


def _allowed(filename: str) -> bool:
    allowed = current_app.config.get("ALLOWED_EXTENSIONS")
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@files_bp.post("")
@jwt_required()
def upload_file_route():
    user_id = get_jwt_identity()
    if "file" not in request.files:
        return {"error": "No file"}, 400
    f = request.files["file"]
    if f.filename == "" or not _allowed(f.filename):
        return {"error": "Invalid file"}, 400

    url, key = upload_file(f)

    obj = FileObject(
        user_id=user_id,
        filename=f.filename,
        url=url,
        mime_type=f.mimetype,
        size_bytes=None,
        is_public=bool(request.form.get("is_public", False)),
        category_id=request.form.get("category_id"),
        page_id=request.form.get("page_id"),
    )
    db.session.add(obj)
    db.session.commit()
    return {"id": obj.id, "url": obj.url}, 201


@files_bp.get("")
@jwt_required()
def list_files():
    user_id = get_jwt_identity()
    files = FileObject.query.filter_by(user_id=user_id).order_by(FileObject.created_at.desc()).all()
    return [
        {
            "id": f.id,
            "filename": f.filename,
            "url": f.url,
            "mime_type": f.mime_type,
            "size_bytes": f.size_bytes,
            "is_public": f.is_public,
            "category_id": f.category_id,
            "page_id": f.page_id,
        }
        for f in files
    ]