from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
from app.utils import file_handler

tasks_bp = Blueprint('tasks', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@tasks_bp.route('/tasks')
@required_login
def index():
    """Tasks page"""
    user_id = session['user_id']
    tasks = file_handler.get_user_tasks(user_id)
    
    # Sort by creation date (newest first)
    tasks = sorted(tasks, key=lambda x: x['created_at'], reverse=True)
    
    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/api/tasks', methods=['GET'])
@required_login
def get_tasks():
    """Get all tasks for user (JSON)"""
    user_id = session['user_id']
    tasks = file_handler.get_user_tasks(user_id)
    
    # Sort by creation date
    tasks = sorted(tasks, key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({'tasks': tasks})


@tasks_bp.route('/api/tasks', methods=['POST'])
@required_login
def create_task():
    """Create a new task"""
    user_id = session['user_id']
    
    # Handle JSON data safely (frontend sends JSON)
    data = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    priority = data.get('priority', 'medium')
    estimate_minutes = data.get('estimate_minutes')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    try:
        estimate_minutes = int(estimate_minutes) if estimate_minutes else None
    except (ValueError, TypeError):
        estimate_minutes = None
    
    task = file_handler.create_task(
        user_id=user_id,
        title=title,
        priority=priority,
        estimate_minutes=estimate_minutes
    )
    
    return jsonify(task), 201


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PATCH', 'PUT'])
@required_login
def update_task(task_id):
    """Update a task"""
    user_id = session['user_id']
    
    # Verify ownership and get data safely
    data = request.get_json(silent=True) or request.form.to_dict() or {}
    task = file_handler.update_task(task_id, **data) if data else None
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task)


@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@required_login
def delete_task(task_id):
    """Delete a task"""
    user_id = session['user_id']
    
    # Verify ownership
    task = next((t for t in file_handler.get_user_tasks(user_id) if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    file_handler.delete_task(task_id)
    return jsonify({'success': True})
