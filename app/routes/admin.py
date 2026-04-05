from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler, analytics_utils

admin_bp = Blueprint('admin', __name__)


def required_admin(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            return redirect(url_for('auth.admin_login'))
        user = file_handler.get_user_by_id(session['user_id'])
        if not user or user['role'] != 'admin':
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/admin')
@admin_bp.route('/admin/dashboard')
@required_admin
def dashboard():
    """Admin dashboard"""
    # Get all users
    users, total = file_handler.get_all_users(limit=1000)
    
    # Filter out admin users
    users = [u for u in users if u['role'] == 'user']
    
    # Get overall analytics
    all_analytics = analytics_utils.get_all_users_analytics(7)
    
    return render_template('admin/dashboard.html', users=users, total=len(users), analytics=all_analytics)


@admin_bp.route('/admin/users')
@required_admin
def users_list():
    """List all users"""
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    limit = 20
    offset = (page - 1) * limit
    
    users, total = file_handler.get_all_users(search=search, limit=limit, offset=offset)
    
    # Filter out admin users
    users = [u for u in users if u['role'] == 'user']
    
    total_pages = (len(users) + limit - 1) // limit if users else 1
    
    return render_template('admin/users_list.html', users=users, page=page, total_pages=total_pages, search=search)


@admin_bp.route('/admin/users/<int:user_id>')
@required_admin
def user_detail(user_id):
    """View detailed analytics for a specific user"""
    user = file_handler.get_user_by_id(user_id)
    
    if not user or user['role'] != 'user':
        return render_template('admin/user_not_found.html'), 404
    
    # Get user data
    tasks = file_handler.get_user_tasks(user_id)
    habits = file_handler.get_user_habits(user_id)
    journal = file_handler.get_user_journal(user_id)
    finance = file_handler.get_user_finances(user_id)
    mood = file_handler.get_user_moods(user_id)
    focus = file_handler.get_user_focus_sessions(user_id)
    
    # Get analytics
    analytics = analytics_utils.get_user_analytics(user_id, 30)
    
    return render_template('admin/user_detail.html', 
                         user=user,
                         tasks=tasks,
                         habits=habits,
                         journal=journal,
                         finance=finance,
                         mood=mood,
                         focus=focus,
                         analytics=analytics)


@admin_bp.route('/api/admin/users', methods=['GET'])
@required_admin
def get_users():
    """Get all users (JSON)"""
    search = request.args.get('search', '')
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    users, total = file_handler.get_all_users(search=search, limit=limit, offset=offset)
    
    # Filter out admin users
    users = [u for u in users if u['role'] == 'user']
    
    return jsonify({'users': users, 'total': len(users)})


@admin_bp.route('/api/admin/analytics', methods=['GET'])
@required_admin
def get_analytics():
    """Get analytics for all users (JSON)"""
    days = request.args.get('days', 7, type=int)
    user_id = request.args.get('user_id', type=int)
    
    if user_id:
        analytics = analytics_utils.get_user_analytics(user_id, days)
    else:
        analytics = analytics_utils.get_all_users_analytics(days)
    
    return jsonify(analytics)
