from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import os
from .config import config
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import werkzeug.exceptions
# Models
from .models import User, Video, Comment, Tag, Short

# Extensions
from .extensions import db, mailer

# Routes
from .routes import auth_route
from .routes import user_route
from .routes import video_route
from .routes import tags_route
from .routes import comment_route
from .routes import reaction_route
load_dotenv()

migrate = Migrate()
jwt_manager = JWTManager()

def create_app(config_mode=None):
    """Return Flask instance"""
    app = Flask(__name__)

    @app.before_request
    def decode_req():
        if request.data:
            request.data = request.data.decode('utf-8')
    # Use default config_mode if not provided

    @app.errorhandler(werkzeug.exceptions.NotFound)
    def handle_404_error(e):
        response = {
            "error": "Not Found",
            "message": "The requested resource was not found.",
            "status": 404
        }
        return jsonify(response), 404


    if config_mode is None:
        config_mode = os.getenv('CONFIG_MODE', 'development')
    
    print(f"Loading configuration for: {config_mode}")
    app.config.from_object(config[config_mode])
    
    # Database
    db.init_app(app)

    # Database migration
    migrate.init_app(app, db)

    # Initializing MAILER
    mailer.init_app(app=app)

    # Initializing JWT
    jwt_manager.init_app(app)


    # Enabling CORS
    CORS(app, supports_credentials=True)
    # Listing controllers
    app.register_blueprint(blueprint=auth_route, url_prefix='/auth')
    app.register_blueprint(blueprint=user_route, url_prefix='/user')
    app.register_blueprint(blueprint=video_route, url_prefix='/video')
    app.register_blueprint(blueprint=tags_route, url_prefix='/tags')
    app.register_blueprint(blueprint=comment_route, url_prefix='/comments')
    app.register_blueprint(blueprint=reaction_route, url_prefix='/reaction')


    return app

