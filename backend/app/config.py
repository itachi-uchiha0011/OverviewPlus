import os
from datetime import timedelta


class Config:
    def __init__(self) -> None:
        self.SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
        self.APP_NAME = os.getenv("APP_NAME", "Overview+")
        self.ENV = os.getenv("ENV", "development")
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"

        # Database
        _db_url = os.getenv("DATABASE_URL", "sqlite:///overview_plus.db")
        if _db_url.startswith("postgresql://") and "+" not in _db_url:
            _db_url = _db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        self.SQLALCHEMY_DATABASE_URI = _db_url
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # JWT
        self.JWT_SECRET_KEY = self.SECRET_KEY
        self.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
        self.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

        # CORS
        self.APP_URL = os.getenv("APP_URL", "http://localhost:5000")
        self.FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
        self.CORS_ORIGINS = [self.APP_URL, self.FRONTEND_URL, "http://127.0.0.1:5173"]

        # Rate Limiting
        self.RATELIMIT_DEFAULT = "200 per hour"
        self.RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

        # Email
        self.SMTP_SERVER = os.getenv("SMTP_SERVER")
        self.SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
        self.SMTP_USER = os.getenv("SMTP_USER")
        self.SMTP_PASS = os.getenv("SMTP_PASS")
        self.EMAIL_FROM = os.getenv("EMAIL_FROM", "no-reply@example.com")
        self.SMTP_DEBUG = os.getenv("SMTP_DEBUG", "0")

        # Telegram
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

        # Storage
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
        self.AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
        self.UPLOAD_FOLDER = os.getenv(
            "UPLOAD_FOLDER",
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads")),
        )
        self.MAX_CONTENT_LENGTH = 20 * 1024 * 1024
        self.ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt"}

        # Web Push
        self.VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
        self.VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
        self.VAPID_EMAIL = os.getenv("VAPID_EMAIL")

        # Preferences
        self.DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
        self.DEFAULT_THEME = os.getenv("DEFAULT_THEME", "light")