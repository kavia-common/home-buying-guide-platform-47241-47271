import os
from flask import Flask
from flask_cors import CORS

def create_app():
    """
    PUBLIC_INTERFACE
    Flask application factory for the Interactive Home Buying Guide backend.

    Returns:
        Flask: Configured Flask app with registered blueprints and CORS.
    """
    app = Flask(__name__)

    # Configuration via environment variables (optional)
    app.config["BACKEND_PORT"] = int(os.getenv("BACKEND_PORT", "3001"))
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

    # Enable CORS for frontend origin
    CORS(app, resources={r"/api/*": {"origins": [frontend_origin]}})

    # Register blueprints
    from .routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/", methods=["GET"])
    def health():
        """
        PUBLIC_INTERFACE
        Health check route.

        Returns:
            dict: Simple health status.
        """
        return {"status": "ok", "service": "interactive_home_buying_guide_backend"}

    return app
