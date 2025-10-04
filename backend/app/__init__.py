from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','))
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Register blueprints
    from .routes.flow import flow_bp
    from .routes.auth import auth_bp
    
    app.register_blueprint(flow_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    return app
