import os
from typing import Tuple
from uuid import uuid4
from werkzeug.datastructures import FileStorage
from flask import current_app
import boto3
from supabase import create_client, Client


def _get_supabase() -> Client | None:
    url = current_app.config.get('SUPABASE_URL')
    key = current_app.config.get('SUPABASE_SERVICE_KEY')
    if not url or not key:
        return None
    return create_client(url, key)


def upload_file(file: FileStorage) -> Tuple[str, str]:
    backend = current_app.config.get('STORAGE_BACKEND', 'local')
    if backend == 's3' and current_app.config.get('AWS_S3_BUCKET'):
        return _upload_s3(file)
    if backend == 'supabase' and _get_supabase():
        return _upload_supabase(file)
    return _upload_local(file)


def _upload_local(file: FileStorage) -> Tuple[str, str]:
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    from werkzeug.utils import secure_filename

    filename = secure_filename(file.filename or f"file_{uuid4().hex}")
    unique_name = f"{uuid4().hex}_{filename}"
    path = os.path.join(upload_dir, unique_name)
    file.save(path)
    url = f"/uploads/{unique_name}"
    return url, unique_name


def _upload_s3(file: FileStorage) -> Tuple[str, str]:
    bucket = current_app.config['AWS_S3_BUCKET']
    region = current_app.config.get('AWS_REGION', 'us-east-1')
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'),
        region_name=region,
    )
    from werkzeug.utils import secure_filename

    filename = secure_filename(file.filename or f"file_{uuid4().hex}")
    key = f"uploads/{uuid4().hex}_{filename}"
    file.stream.seek(0)
    s3.upload_fileobj(file, bucket, key, ExtraArgs={'ACL': 'public-read', 'ContentType': file.mimetype or 'application/octet-stream'})
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
    return url, key


def _upload_supabase(file: FileStorage) -> Tuple[str, str]:
    sb = _get_supabase()
    assert sb is not None
    bucket = current_app.config.get('SUPABASE_BUCKET', 'public')
    from werkzeug.utils import secure_filename

    filename = secure_filename(file.filename or f"file_{uuid4().hex}")
    key = f"uploads/{uuid4().hex}_{filename}"
    file.stream.seek(0)
    sb.storage.from_(bucket).upload(file=file, path=key, file_options={"content-type": file.mimetype or 'application/octet-stream', "upsert": True})
    public_url = sb.storage.from_(bucket).get_public_url(key)
    return public_url, key


def delete_file(key_or_name: str) -> None:
    backend = current_app.config.get('STORAGE_BACKEND', 'local')
    if backend == 's3' and current_app.config.get('AWS_S3_BUCKET') and not key_or_name.startswith('/'):
        bucket = current_app.config['AWS_S3_BUCKET']
        s3 = boto3.client(
            's3',
            aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'),
            region_name=current_app.config.get('AWS_REGION', 'us-east-1'),
        )
        try:
            s3.delete_object(Bucket=bucket, Key=key_or_name)
        except Exception:
            pass
    elif backend == 'supabase' and _get_supabase():
        try:
            sb = _get_supabase()
            bucket = current_app.config.get('SUPABASE_BUCKET', 'public')
            key = key_or_name if not key_or_name.startswith('/') else key_or_name.split('/uploads/',1)[-1]
            sb.storage.from_(bucket).remove([key])
        except Exception:
            pass
    else:
        upload_dir = current_app.config['UPLOAD_FOLDER']
        name = key_or_name.rsplit('/', 1)[-1]
        path = os.path.join(upload_dir, name)
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass