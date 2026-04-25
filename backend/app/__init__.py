from flask import Flask
from flask_cors import CORS
from .config import config
from .db import db, init_db

def create_app(config_name='development'):
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['FRONTEND_URLS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Initialize database
    init_db(app)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.settings import settings_bp
    from .routes.game import game_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(game_bp, url_prefix='/api/game')

    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Chess API is running'}, 200

    return app
