"""
Error Handlers for Flask Application
Handles 404, 500, and other HTTP errors gracefully
"""

from flask import render_template, jsonify
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Register error handlers with the Flask app"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors"""
        logger.warning(f"404 error: {error}")
        if request_wants_json():
            return jsonify({'error': 'Not found', 'status': 404}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors"""
        logger.error(f"500 error: {error}", exc_info=True)
        if request_wants_json():
            return jsonify({'error': 'Internal server error', 'status': 500}), 500
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 Forbidden errors"""
        logger.warning(f"403 error: {error}")
        if request_wants_json():
            return jsonify({'error': 'Forbidden', 'status': 403}), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Handle 401 Unauthorized errors"""
        logger.warning(f"401 error: {error}")
        if request_wants_json():
            return jsonify({'error': 'Unauthorized', 'status': 401}), 401
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle 400 Bad Request errors"""
        logger.warning(f"400 error: {error}")
        if request_wants_json():
            return jsonify({'error': 'Bad request', 'status': 400}), 400
        return render_template('errors/400.html'), 400


def request_wants_json():
    """Check if the request wants JSON response"""
    from flask import request
    # Check if request path is /api/ or if JSON is preferred in Accept header
    if request.path.startswith('/api/'):
        return True
    
    # Check Accept header - this is a simpler approach
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and request.accept_mimetypes[best] >= request.accept_mimetypes['text/html']
