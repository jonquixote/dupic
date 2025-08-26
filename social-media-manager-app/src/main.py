import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv
from .models import db

# Import blueprints with explicit type hints
from .routes.ai_configs import ai_configs_bp
from .routes.video_analysis import video_analysis_bp
from .routes.user_analytics import user_analytics_bp
from .routes.favorite_content import favorite_content_bp
from .routes.characters import characters_bp
from .routes.api_keys import api_keys_bp
from .routes.content_generation import content_generation_bp
from .routes.trends import trends_bp

# Ensure all blueprints are Blueprint instances (not _DummyBlueprint)
assert isinstance(ai_configs_bp, Blueprint)
assert isinstance(video_analysis_bp, Blueprint)
assert isinstance(user_analytics_bp, Blueprint)
assert isinstance(favorite_content_bp, Blueprint)
assert isinstance(characters_bp, Blueprint)
assert isinstance(api_keys_bp, Blueprint)
assert isinstance(content_generation_bp, Blueprint)
assert isinstance(trends_bp, Blueprint)

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media_manager.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(ai_configs_bp, url_prefix='/api')
    app.register_blueprint(video_analysis_bp, url_prefix='/api')
    app.register_blueprint(user_analytics_bp, url_prefix='/api')
    app.register_blueprint(favorite_content_bp, url_prefix='/api')
    app.register_blueprint(characters_bp, url_prefix='/api')
    app.register_blueprint(api_keys_bp, url_prefix='/api')
    app.register_blueprint(content_generation_bp, url_prefix='/api')
    app.register_blueprint(trends_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'AI Social Media Manager API is running'})
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Welcome to the AI Social Media Manager API',
            'version': '2.0.0',
            'endpoints': {
                'health': '/api/health',
                'users': '/api/users',
                'ai_configs': '/api/ai-configs',
                'video_analysis': '/api/video-analysis',
                'user_analytics': '/api/user-analytics',
                'favorite_content': '/api/favorite-content',
                'characters': '/api/characters',
                'api_keys': '/api/api_keys',
                'content_generation': '/api/content/generate',
                'trends': '/api/trends'
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
