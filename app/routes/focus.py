from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler

focus_bp = Blueprint('focus', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@focus_bp.route('/focus')
@required_login
def index():
    """Focus sessions page"""
    user_id = session['user_id']
    sessions = file_handler.get_user_focus_sessions(user_id)
    
    # Sort by creation date (newest first)
    sessions = sorted(sessions, key=lambda x: x['created_at'], reverse=True)
    
    total_minutes = sum(s['minutes'] for s in sessions)
    
    return render_template('focus.html', sessions=sessions, total_minutes=total_minutes)


@focus_bp.route('/api/focus', methods=['GET'])
@required_login
def get_sessions():
    """Get all focus sessions (JSON)"""
    user_id = session['user_id']
    sessions = file_handler.get_user_focus_sessions(user_id)
    
    # Sort by creation date
    sessions = sorted(sessions, key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'sessions': sessions})


@focus_bp.route('/api/focus', methods=['POST'])
@required_login
def create_session():
    """Create a new focus session"""
    user_id = session['user_id']
    
    data = request.get_json(silent=True) or request.form
    minutes = data.get('minutes')
    
    if not minutes:
        return jsonify({'error': 'Minutes is required'}), 400
    
    try:
        minutes = int(minutes)
        if minutes <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Minutes must be a positive number'}), 400
    
    session_obj = file_handler.create_focus_session(
        user_id=user_id,
        minutes=minutes
    )
    
    return jsonify(session_obj), 201
