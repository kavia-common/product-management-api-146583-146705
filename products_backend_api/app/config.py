import os
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration loaded from environment variables."""
    # API/OpenAPI metadata using Ocean Professional theme
    API_TITLE: str = os.getenv("API_TITLE", "Products API - Ocean Professional")
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION: str = os.getenv("OPENAPI_VERSION", "3.0.3")
    OPENAPI_URL_PREFIX: str = os.getenv("OPENAPI_URL_PREFIX", "/docs")
    OPENAPI_SWAGGER_UI_PATH: str = os.getenv("OPENAPI_SWAGGER_UI_PATH", "")
    OPENAPI_SWAGGER_UI_URL: str = os.getenv(
        "OPENAPI_SWAGGER_UI_URL",
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    # Database connection (use env from products_database container)
    # Do not hardcode secrets; expect DATABASE_URL or individual parts to be provided.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # If DATABASE_URL is not provided, try constructing from parts
    DB_DRIVER: str = os.getenv("DB_DRIVER", "postgresql")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # Pagination defaults
    DEFAULT_PAGE: int = int(os.getenv("DEFAULT_PAGE", "1"))
    DEFAULT_PAGE_SIZE: int = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))

    # Flask
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


def build_database_url(cfg: Config) -> str:
    """Helper to compute a SQLAlchemy-compatible DB URL."""
    if cfg.DATABASE_URL:
        return cfg.DATABASE_URL

    if all([cfg.DB_DRIVER, cfg.DB_HOST, cfg.DB_PORT, cfg.DB_NAME, cfg.DB_USER]):
        if cfg.DB_PASSWORD:
            return f"{cfg.DB_DRIVER}://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}"
        return f"{cfg.DB_DRIVER}://{cfg.DB_USER}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}"

    # As a safe fallback for local dev, use SQLite in-memory (not for production)
    # CI will still boot the app; real deployments should provide DB env vars.
    return "sqlite+pysqlite:///:memory:"
