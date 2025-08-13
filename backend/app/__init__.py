import os
from datetime import timedelta
from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate, jwt, cors, limiter, socketio


def create_app(config_object: type[Config] | None = None) -> Flask:
    load_dotenv()
    app = Flask(__name__)

    # Config
    app.config.from_object(config_object or Config())

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})
    limiter.init_app(app)
    socketio.init_app(app, cors_allowed_origins=app.config.get("CORS_ORIGINS", "*"))

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.users import users_bp
    from .routes.habits import habits_bp
    from .routes.journal import journal_bp
    from .routes.categories import categories_bp
    from .routes.pages import pages_bp
    from .routes.dashboard import dashboard_bp
    from .routes.posts import posts_bp
    from .routes.files import files_bp
    from .routes.todos import todos_bp
    from .routes.channels import channels_bp
    from .routes.alerts import alerts_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(habits_bp, url_prefix="/api/habits")
    app.register_blueprint(journal_bp, url_prefix="/api/journal")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(pages_bp, url_prefix="/api/pages")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(posts_bp, url_prefix="/api/posts")
    app.register_blueprint(files_bp, url_prefix="/api/files")
    app.register_blueprint(todos_bp, url_prefix="/api/todos")
    app.register_blueprint(channels_bp, url_prefix="/api/channels")
    app.register_blueprint(alerts_bp, url_prefix="/api/alerts")

    # Load Socket.IO event handlers
    from .sockets import chat as _chat_handlers  # noqa: F401

    # Simple health check
    @app.get("/api/health")
    def health():
        return {"status": "ok", "app": app.config.get("APP_NAME", "Overview+")}

    # Serve uploaded files (dev/local)
    from flask import send_from_directory

    upload_dir = app.config.get("UPLOAD_FOLDER")
    os.makedirs(upload_dir, exist_ok=True)

    @app.get("/uploads/<path:filename>")
    def uploads(filename: str):
        return send_from_directory(upload_dir, filename)

    return app