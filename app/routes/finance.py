from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler

finance_bp = Blueprint('finance', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@finance_bp.route('/finance')
@required_login
def index():
    """Finance page"""
    user_id = session['user_id']
    entries = file_handler.get_user_finances(user_id)
    
    # Sort by creation date (newest first)
    entries = sorted(entries, key=lambda x: x['created_at'], reverse=True)
    
    categories = ['food', 'transport', 'entertainment', 'utilities', 'healthcare', 'education', 'other']
    
    return render_template('finance.html', entries=entries, categories=categories)


@finance_bp.route('/api/finance', methods=['GET'])
@required_login
def get_finance():
    """Get all finance entries (JSON)"""
    user_id = session['user_id']
    entries = file_handler.get_user_finances(user_id)
    
    # Sort by creation date
    entries = sorted(entries, key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'entries': entries})


@finance_bp.route('/api/finance', methods=['POST'])
@required_login
def create_entry():
    """Create a new finance entry"""
    user_id = session['user_id']
    
    data = request.get_json(silent=True) or request.form
    amount = data.get('amount')
    category = (data.get('category') or '').strip()
    note = data.get('note', '')
    
    if not amount or not category:
        return jsonify({'error': 'Amount and category are required'}), 400
    
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount'}), 400
    
    entry = file_handler.create_finance_entry(
        user_id=user_id,
        amount=amount,
        category=category,
        note=note
    )
    
    return jsonify(entry), 201
