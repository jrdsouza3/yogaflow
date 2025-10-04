from flask import Flask
from flask_cors import CORS
import os
from .config import config

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Configure CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from .routes.flow import flow_bp
    from .routes.auth import auth_bp
    
    app.register_blueprint(flow_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    return app
