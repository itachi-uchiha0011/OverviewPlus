import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    APP_NAME = os.getenv("APP_NAME", "Overview+")
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # Database
    _db_url = os.getenv("DATABASE_URL", "sqlite:///overview_plus.db")
    if _db_url.startswith("postgresql://") and "+" not in _db_url:
        # Prefer psycopg3 driver if installed
        _db_url = _db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # CORS
    APP_URL = os.getenv("APP_URL", "http://localhost:5000")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    CORS_ORIGINS = [APP_URL, FRONTEND_URL, "http://127.0.0.1:5173"]

    # Rate Limiting
    RATELIMIT_DEFAULT = "200 per hour"
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

    # Email
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASS = os.getenv("SMTP_PASS")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "no-reply@example.com")

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

    # Storage
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads")))
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt"}

    # Web Push
    VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
    VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
    VAPID_EMAIL = os.getenv("VAPID_EMAIL")

    # Preferences
    DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
    DEFAULT_THEME = os.getenv("DEFAULT_THEME", "light")