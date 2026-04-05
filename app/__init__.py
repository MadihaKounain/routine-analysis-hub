from flask import Flask
from app.routes import auth, dashboard, tasks, journal, finance, mood, habits, focus, admin, chatbot
from app.utils.logger import setup_logging
from app.utils.errors import register_error_handlers
import sys
import os
from dotenv import load_dotenv

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file with explicit path
env_file = os.path.join(project_root, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)

sys.path.insert(0, project_root)
from config import get_config


def create_app(env=None):
    """Create and configure the Flask application
    
    Args:
        env: Environment name (development, testing, production)
             If None, uses FLASK_ENV environment variable
    """
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')
    
    # Load configuration from config.py
    config = get_config(env)
    app.config.from_object(config)
    
    # Setup logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(dashboard.dashboard_bp)
    app.register_blueprint(tasks.tasks_bp)
    app.register_blueprint(journal.journal_bp)
    app.register_blueprint(finance.finance_bp)
    app.register_blueprint(mood.mood_bp)
    app.register_blueprint(habits.habits_bp)
    app.register_blueprint(focus.focus_bp)
    app.register_blueprint(admin.admin_bp)
    app.register_blueprint(chatbot.chatbot_bp)
    
    app.logger.debug(f"Flask app created in {config.__class__.__name__} mode")
    
    return app
