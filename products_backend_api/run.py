import os
from app import create_app  # type: ignore

# PUBLIC_INTERFACE
app = create_app()

if __name__ == "__main__":
    """Entrypoint to run the Flask application."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "3001"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
