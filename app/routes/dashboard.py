from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler, analytics_utils
from dateutil import parser as dateutil_parser
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@dashboard_bp.route('/dashboard')
@dashboard_bp.route('/')
def index():
    """Dashboard or landing page"""
    if 'user_id' not in session:
        return render_template('landing.html')
    
    user_id = session['user_id']
    
    # Get analytics
    analytics = analytics_utils.get_user_analytics(user_id, 7)
    
    return render_template('dashboard.html', analytics=analytics)


@dashboard_bp.route('/api/analytics', methods=['GET'])
@required_login
def get_analytics():
    """Get analytics data (JSON for AJAX)"""
    user_id = session['user_id']
    days = request.args.get('days', 7, type=int)
    
    analytics = analytics_utils.get_user_analytics(user_id, days)
    return jsonify(analytics)
