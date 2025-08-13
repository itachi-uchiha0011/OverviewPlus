from __future__ import with_statement
from logging.config import fileConfig
from alembic import context
import os
import sys

# add project path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.extensions import db

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_app():
    return create_app()


def get_target_metadata():
    return db.metadata


def run_migrations_offline() -> None:
    app = get_app()
    with app.app_context():
        url = os.getenv("DATABASE_URL", app.config.get("SQLALCHEMY_DATABASE_URI"))
        context.configure(
            url=url,
            target_metadata=get_target_metadata(),
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online() -> None:
    app = get_app()
    with app.app_context():
        connection = db.engine.connect()
        context.configure(connection=connection, target_metadata=get_target_metadata())
        try:
            with context.begin_transaction():
                context.run_migrations()
        finally:
            connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()