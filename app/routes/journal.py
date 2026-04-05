from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler

journal_bp = Blueprint('journal', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@journal_bp.route('/journal')
@required_login
def index():
    """Journal page"""
    user_id = session['user_id']
    entries = file_handler.get_user_journal(user_id)
    
    # Sort by creation date (newest first)
    entries = sorted(entries, key=lambda x: x['created_at'], reverse=True)
    
    return render_template('journal.html', entries=entries)


@journal_bp.route('/api/journal', methods=['GET'])
@required_login
def get_journal():
    """Get all journal entries (JSON)"""
    user_id = session['user_id']
    entries = file_handler.get_user_journal(user_id)
    
    # Sort by creation date
    entries = sorted(entries, key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'entries': entries})


@journal_bp.route('/api/journal', methods=['POST'])
@required_login
def create_entry():
    """Create a new journal entry"""
    user_id = session['user_id']
    
    data = request.get_json(silent=True) or request.form
    content = data.get('content', '')
    mood = data.get('mood')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    try:
        mood = int(mood) if mood else None
    except (ValueError, TypeError):
        mood = None
    
    entry = file_handler.create_journal_entry(
        user_id=user_id,
        content=content,
        mood=mood
    )
    
    return jsonify(entry), 201
