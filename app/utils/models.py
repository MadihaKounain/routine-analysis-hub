"""
Data Models Documentation
Describes the structure of all data collections in the JSON database
"""

# User Model
USER_MODEL = {
    'id': int,
    'username': str,
    'email': str,
    'password_hash': str,
    'created_at': str,  # ISO 8601 format
    'role': str  # 'user' or 'admin'
}

# Task Model
TASK_MODEL = {
    'id': int,
    'user_id': int,
    'title': str,
    'description': str,
    'priority': str,  # 'low', 'medium', 'high'
    'status': str,  # 'pending', 'completed'
    'due_date': str,  # ISO 8601 format or null
    'created_at': str,
    'completed_at': str  # null if not completed
}

# Habit Model
HABIT_MODEL = {
    'id': int,
    'user_id': int,
    'name': str,
    'description': str,
    'frequency': str,  # 'daily', 'weekly', etc
    'created_at': str,
    'completions': [str]  # List of dates (ISO 8601) when completed
}

# Journal Model
JOURNAL_MODEL = {
    'id': int,
    'user_id': int,
    'title': str,
    'content': str,
    'mood': int,  # 1-10 scale
    'word_count': int,
    'tags': [str],
    'created_at': str
}

# Finance Model
FINANCE_MODEL = {
    'id': int,
    'user_id': int,
    'amount': float,
    'category': str,  # 'food', 'transport', 'entertainment', etc
    'description': str,
    'notes': str,
    'created_at': str
}

# Mood Model
MOOD_MODEL = {
    'id': int,
    'user_id': int,
    'mood': int,  # 1-10 scale
    'notes': str,
    'created_at': str
}

# Focus Model
FOCUS_MODEL = {
    'id': int,
    'user_id': int,
    'duration': int,  # Duration in minutes
    'notes': str,
    'created_at': str
}

"""
DATABASE STRUCTURE (app/database/app.json):

{
    "users": [USER_MODEL, ...],
    "tasks": [TASK_MODEL, ...],
    "habits": [HABIT_MODEL, ...],
    "journal": [JOURNAL_MODEL, ...],
    "finance": [FINANCE_MODEL, ...],
    "mood": [MOOD_MODEL, ...],
    "focus": [FOCUS_MODEL, ...]
}
"""
