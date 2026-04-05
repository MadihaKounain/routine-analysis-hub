from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler

mood_bp = Blueprint('mood', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@mood_bp.route('/mood')
@required_login
def index():
    """Mood tracking page"""
    user_id = session['user_id']
    moods = file_handler.get_user_moods(user_id)
    
    # Sort by creation date (newest first)
    moods = sorted(moods, key=lambda x: x['created_at'], reverse=True)
    
    return render_template('mood.html', moods=moods)


@mood_bp.route('/api/mood', methods=['GET'])
@required_login
def get_moods():
    """Get all mood entries (JSON)"""
    user_id = session['user_id']
    moods = file_handler.get_user_moods(user_id)
    
    # Sort by creation date
    moods = sorted(moods, key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'moods': moods})


@mood_bp.route('/api/mood', methods=['POST'])
@required_login
def create_mood():
    """Create a new mood entry"""
    user_id = session['user_id']
    
    data = request.get_json(silent=True) or request.form
    mood_value = data.get('mood')
    note = data.get('note', '')
    
    if not mood_value:
        return jsonify({'error': 'Mood is required'}), 400
    
    try:
        mood_value = int(mood_value)
        if mood_value < 1 or mood_value > 10:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Mood must be between 1 and 10'}), 400
    
    mood = file_handler.create_mood_entry(
        user_id=user_id,
        mood_value=mood_value,
        note=note
    )
    
    return jsonify(mood), 201
