"""
Logging Configuration for Production and Development
Provides structured logging with file rotation and console output
"""

import logging
import logging.handlers
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import get_config


def setup_logging(app):
    """
    Configure logging for the Flask application
    
    Args:
        app: Flask application instance
    """
    
    config = get_config()
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Get log level
    log_level = getattr(logging, config.LOG_LEVEL, logging.INFO)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s in %(module)s:%(funcName)s(%(lineno)d): %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File Handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(detailed_formatter)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configure Flask app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # Reduce noise from werkzeug (Flask's development server logger)
    if not app.debug:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    app.logger.info(f"Logging initialized - Level: {config.LOG_LEVEL}, File: {config.LOG_FILE}")
    
    return app.logger
