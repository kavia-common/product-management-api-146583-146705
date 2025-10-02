from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from sqlalchemy import text

from .config import Config
from .db import db
from .routes.health import blp as health_blp
from .routes.products import blp as products_blp


def _configure_openapi(app: Flask) -> None:
    """Apply OpenAPI and API metadata from config."""
    cfg = Config()
    app.config["API_TITLE"] = cfg.API_TITLE
    app.config["API_VERSION"] = cfg.API_VERSION
    app.config["OPENAPI_VERSION"] = cfg.OPENAPI_VERSION
    app.config["OPENAPI_URL_PREFIX"] = cfg.OPENAPI_URL_PREFIX
    app.config["OPENAPI_SWAGGER_UI_PATH"] = cfg.OPENAPI_SWAGGER_UI_PATH
    app.config["OPENAPI_SWAGGER_UI_URL"] = cfg.OPENAPI_SWAGGER_UI_URL


def _configure_db(app: Flask) -> None:
    """Initialize SQLAlchemy with connection from environment."""
    from .config import build_database_url

    app.config["SQLALCHEMY_DATABASE_URI"] = build_database_url(Config())
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # Create tables if using SQLite fallback (no-op for managed DBs)
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            # If DB is external and managed, ignore create_all failure
            pass


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Create and configure the Flask application with CORS, OpenAPI, DB, and routes."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/*": {"origins": "*"}})

    _configure_openapi(app)
    _configure_db(app)

    api = Api(app)

    # Register blueprints
    api.register_blueprint(health_blp)
    api.register_blueprint(products_blp)

    return app
