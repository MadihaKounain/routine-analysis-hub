"""
Custom Decorators for Flask Routes
Handles authentication, authorization, logging, and error handling
"""

from functools import wraps
from flask import session, redirect, url_for, jsonify, request
import logging

logger = logging.getLogger(__name__)


def required_login(f):
    """Decorator to require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            logger.warning(f"Unauthorized access attempt to {request.path} from {request.remote_addr}")
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def required_admin(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            logger.warning(f"Unauthorized admin access attempt from {request.remote_addr}")
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('auth.admin_login'))
        
        # Check if user is admin
        if not session.get('is_admin'):
            logger.warning(f"Non-admin user {session.get('user_id')} attempted admin access to {request.path}")
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Forbidden'}), 403
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function


def log_request(f):
    """Decorator to log all requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.debug(f"{request.method} {request.path} from {request.remote_addr}")
        return f(*args, **kwargs)
    return decorated_function


def handle_json_errors(f):
    """Decorator to handle JSON response errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Internal server error'}), 500
            raise
    return decorated_function
