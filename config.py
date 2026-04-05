"""
Flask Configuration Management
Supports multiple environments: development, testing, production
"""

import os
from datetime import timedelta


class Config:
    """Base configuration - common settings for all environments"""
    
    # Flask Core
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'app/database/app.json')
    
    # Application
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = False
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 10
    
    # Security
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
    LOG_LEVEL = 'DEBUG'
    
    # Disable caching for development
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestingConfig(Config):
    """Testing configuration"""
    
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False
    DATABASE_PATH = 'tests/test_db.json'
    LOG_LEVEL = 'DEBUG'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    PROPAGATE_EXCEPTIONS = True
    LOG_LEVEL = 'WARNING'
    
    def __init__(self):
        # Require SECRET_KEY in production
        if not os.getenv('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable required in production")


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration for specified environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])
