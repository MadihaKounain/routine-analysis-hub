from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils import file_handler, auth_utils
from functools import wraps

auth_bp = Blueprint('auth', __name__)


def required_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def required_admin(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.admin_login'))
        user = file_handler.get_user_by_id(session['user_id'])
        if not user or user['role'] != 'admin':
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        
        if error is None:
            if file_handler.get_user_by_username(username):
                error = 'Username already exists.'
            elif file_handler.get_user_by_email(email):
                error = 'Email already exists.'
        
        if error is None:
            password_hash = auth_utils.hash_password(password)
            user = file_handler.create_user(username, email, password_hash)
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard.index'))
        
        return render_template('register.html', error=error)
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        identity = request.form.get('identity', '').strip()
        password = request.form.get('password', '')
        
        error = None
        user = None
        
        if not identity:
            error = 'Username or email is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = file_handler.get_user_by_username(identity)
            if not user:
                user = file_handler.get_user_by_email(identity)
        
        if user is None:
            error = 'Invalid username or email.'
        elif not auth_utils.verify_password(password, user['password_hash']):
            error = 'Invalid password.'
        elif user['role'] != 'user':
            error = 'Only regular users can log in here. Admins use the admin panel.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard.index'))
        
        return render_template('login.html', error=error)
    
    return render_template('login.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        error = None
        user = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = file_handler.get_user_by_username(username)
        
        if user is None:
            error = 'Invalid username.'
        elif user['role'] != 'admin':
            error = 'This account is not an admin account.'
        elif not auth_utils.verify_password(password, user['password_hash']):
            error = 'Invalid password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = True
            admin_token = auth_utils.sign_admin_token(user['id'], user['username'])
            session['admin_token'] = admin_token
            return redirect(url_for('admin.dashboard'))
        
        return render_template('admin_login.html', error=error)
    
    return render_template('admin_login.html')


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('auth.login'))
