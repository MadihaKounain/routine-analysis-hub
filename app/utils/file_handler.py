import json
import os
from datetime import datetime
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent.parent / 'database' / 'app.json'

# Ensure database directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Default database structure
DEFAULT_DB = {
    "users": [],
    "tasks": [],
    "habits": [],
    "journal": [],
    "finance": [],
    "mood": [],
    "focus": []
}


def initialize_db():
    """Initialize database if it doesn't exist"""
    if not DB_PATH.exists():
        write_json(DEFAULT_DB)


def read_json():
    """Read the entire JSON database"""
    try:
        if not DB_PATH.exists():
            initialize_db()
        with open(DB_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        initialize_db()
        return DEFAULT_DB.copy()


def write_json(data):
    """Write data to JSON database"""
    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DB_PATH, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error writing to database: {e}")
        raise


def get_next_id(collection_name):
    """Get the next available ID for a collection"""
    db = read_json()
    collection = db.get(collection_name, [])
    if not collection:
        return 1
    return max([item.get('id', 0) for item in collection]) + 1


# User operations
def get_user_by_email(email):
    """Get user by email"""
    db = read_json()
    for user in db.get('users', []):
        if user['email'].lower() == email.lower():
            return user
    return None


def get_user_by_username(username):
    """Get user by username"""
    db = read_json()
    for user in db.get('users', []):
        if user['username'].lower() == username.lower():
            return user
    return None


def get_user_by_id(user_id):
    """Get user by ID"""
    db = read_json()
    for user in db.get('users', []):
        if user['id'] == user_id:
            return user
    return None


def create_user(username, email, password_hash, role='user'):
    """Create a new user"""
    db = read_json()
    user_id = get_next_id('users')
    user = {
        'id': user_id,
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'role': role,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    db['users'].append(user)
    write_json(db)
    return user


def get_all_users(search='', min_id=None, max_id=None, limit=100, offset=0):
    """Get all users with optional filtering"""
    db = read_json()
    users = db.get('users', [])
    
    # Filter by search term
    if search:
        search_lower = search.lower()
        users = [u for u in users if search_lower in u['username'].lower() or search_lower in u['email'].lower()]
    
    # Filter by ID range
    if min_id is not None:
        users = [u for u in users if u['id'] >= min_id]
    if max_id is not None:
        users = [u for u in users if u['id'] <= max_id]
    
    # Sort by ID
    users = sorted(users, key=lambda x: x['id'])
    
    # Pagination
    total = len(users)
    paginated = users[offset:offset + limit]
    
    return paginated, total


# Task operations
def get_user_tasks(user_id):
    """Get all tasks for a user"""
    db = read_json()
    tasks = db.get('tasks', [])
    return [t for t in tasks if t['user_id'] == user_id]


def create_task(user_id, title, status='pending', priority='medium', estimate_minutes=None, actual_minutes=None):
    """Create a new task"""
    db = read_json()
    task_id = get_next_id('tasks')
    task = {
        'id': task_id,
        'user_id': user_id,
        'title': title,
        'status': status,
        'priority': priority,
        'estimate_minutes': estimate_minutes,
        'actual_minutes': actual_minutes,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'completed_at': None
    }
    db['tasks'].append(task)
    write_json(db)
    return task


def update_task(task_id, **kwargs):
    """Update a task"""
    db = read_json()
    for task in db['tasks']:
        if task['id'] == task_id:
            if kwargs.get('status') == 'completed':
                task['completed_at'] = datetime.utcnow().isoformat() + 'Z'
            task.update(kwargs)
            write_json(db)
            return task
    return None


def delete_task(task_id):
    """Delete a task"""
    db = read_json()
    db['tasks'] = [t for t in db['tasks'] if t['id'] != task_id]
    write_json(db)


# Habit operations
def get_user_habits(user_id):
    """Get all habit entries for a user"""
    db = read_json()
    habits = db.get('habits', [])
    return [h for h in habits if h['user_id'] == user_id]


def create_habit(user_id, habit_name):
    """Create a new habit completion entry"""
    db = read_json()
    habit_id = get_next_id('habits')
    habit = {
        'id': habit_id,
        'user_id': user_id,
        'habit_name': habit_name,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    db['habits'].append(habit)
    write_json(db)
    return habit


def get_habit_streak(user_id, habit_name):
    """Calculate current streak for a habit"""
    habits = get_user_habits(user_id)
    habit_entries = [h for h in habits if h['habit_name'] == habit_name]
    habit_entries = sorted(habit_entries, key=lambda x: x['created_at'], reverse=True)
    
    if not habit_entries:
        return 0
    
    streak = 0
    expected_date = datetime.utcnow().date()
    
    for entry in habit_entries:
        entry_date = datetime.fromisoformat(entry['created_at'].replace('Z', '+00:00')).date()
        if entry_date == expected_date:
            streak += 1
            expected_date = expected_date - __import__('datetime').timedelta(days=1)
        else:
            break
    
    return streak


# Journal operations
def get_user_journal(user_id):
    """Get all journal entries for a user"""
    db = read_json()
    journal = db.get('journal', [])
    return [j for j in journal if j['user_id'] == user_id]


def create_journal_entry(user_id, content, mood=None):
    """Create a new journal entry"""
    db = read_json()
    entry_id = get_next_id('journal')
    word_count = len(content.split()) if content else 0
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'content': content,
        'mood': mood,
        'word_count': word_count,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    db['journal'].append(entry)
    write_json(db)
    return entry


# Finance operations
def get_user_finances(user_id):
    """Get all finance entries for a user"""
    db = read_json()
    finance = db.get('finance', [])
    return [f for f in finance if f['user_id'] == user_id]


def create_finance_entry(user_id, amount, category, note=None):
    """Create a new finance entry"""
    db = read_json()
    entry_id = get_next_id('finance')
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'amount': amount,
        'category': category,
        'note': note,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    db['finance'].append(entry)
    write_json(db)
    return entry


# Mood operations
def get_user_moods(user_id):
    """Get all mood entries for a user"""
    db = read_json()
    moods = db.get('mood', [])
    return [m for m in moods if m['user_id'] == user_id]


def create_mood_entry(user_id, mood_value, note=None):
    """Create a new mood entry"""
    db = read_json()
    entry_id = get_next_id('mood')
    entry = {
        'id': entry_id,
        'user_id': user_id,
        'mood': mood_value,
        'note': note,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    db['mood'].append(entry)
    write_json(db)
    return entry


# Focus sessions operations
def get_user_focus_sessions(user_id):
    """Get all focus sessions for a user"""
    db = read_json()
    focus = db.get('focus', [])
    return [f for f in focus if f['user_id'] == user_id]


def create_focus_session(user_id, minutes):
    """Create a new focus session"""
    db = read_json()
    session_id = get_next_id('focus')
    session = {
        'id': session_id,
        'user_id': user_id,
        'minutes': minutes,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    db['focus'].append(session)
    write_json(db)
    return session


# Initialize database on import
initialize_db()
