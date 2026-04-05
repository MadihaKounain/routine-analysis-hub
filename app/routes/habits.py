from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler

habits_bp = Blueprint('habits', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@habits_bp.route('/habits')
@required_login
def index():
    """Habits page"""
    user_id = session['user_id']
    
    # Get habit completions
    habits = file_handler.get_user_habits(user_id)
    
    # Get unique habit names with streak info
    habit_names = set(h['habit_name'] for h in habits)
    habit_data = []
    
    for habit_name in habit_names:
        habit_entries = [h for h in habits if h['habit_name'] == habit_name]
        habit_entries = sorted(habit_entries, key=lambda x: x['created_at'], reverse=True)
        
        streak = file_handler.get_habit_streak(user_id, habit_name)
        total = len(habit_entries)
        
        habit_data.append({
            'name': habit_name,
            'streak': streak,
            'total': total,
            'recent_entries': habit_entries[:7]  # Last 7 entries
        })
    
    # Sort by recency
    habit_data = sorted(habit_data, key=lambda x: x['recent_entries'][0]['created_at'] if x['recent_entries'] else '', reverse=True)
    
    return render_template('habits.html', habits=habit_data)


@habits_bp.route('/api/habits', methods=['GET'])
@required_login
def get_habits():
    """Get all habits (JSON)"""
    user_id = session['user_id']
    habits = file_handler.get_user_habits(user_id)
    
    return jsonify({'habits': habits})


@habits_bp.route('/api/habits', methods=['POST'])
@required_login
def create_habit():
    """Create/log a new habit completion"""
    user_id = session['user_id']
    
    data = request.get_json(silent=True) or request.form
    habit_name = (data.get('habit_name') or '').strip()
    
    if not habit_name:
        return jsonify({'error': 'Habit name is required'}), 400
    
    habit = file_handler.create_habit(
        user_id=user_id,
        habit_name=habit_name
    )
    
    return jsonify(habit), 201
