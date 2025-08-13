import os
from datetime import timedelta
from flask import Flask, request
from dotenv import load_dotenv, find_dotenv

from .config import Config
from .extensions import db, migrate, jwt, cors, limiter, socketio
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from .utils.csrf import validate_csrf


def create_app(config_object: type[Config] | None = None) -> Flask:
    load_dotenv(find_dotenv())
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

    # CSRF enforcement for mutating requests
    @app.before_request
    def _csrf_protect():
        if request.method in {"POST", "PUT", "PATCH", "DELETE"} and request.path.startswith('/api/'):
            # Exempt auth endpoints that need to work without CSRF
            if any(request.path.startswith(p) for p in [
                '/api/auth/login', '/api/auth/register', '/api/auth/refresh', '/api/auth/forgot-password', '/api/auth/reset-password'
            ]):
                return
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
            except Exception:
                return {"error": "Unauthorized"}, 401
            token = request.headers.get('X-CSRF-Token')
            if not validate_csrf(user_id, token):
                return {"error": "CSRF"}, 403

    # Start scheduler
    from .scheduler import start_alert_scheduler
    start_alert_scheduler(app)

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
    from .routes.push import push_bp

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
    app.register_blueprint(push_bp, url_prefix="/api/push")

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