#!/usr/bin/env python
"""Seed database with sample data"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils import file_handler

def seed_users():
    """Create sample users"""
    print("Creating sample users...")
    
    users = [
        ('john_doe', 'john@example.com'),
        ('jane_smith', 'jane@example.com'),
        ('alex_kumar', 'alex@example.com'),
    ]
    
    from app.utils import auth_utils
    for username, email in users:
        if not file_handler.get_user_by_username(username):
            password_hash = auth_utils.hash_password('password123')
            user = file_handler.create_user(username, email, password_hash)
            print(f"   ✓ Created user: {username}")
        else:
            print(f"   - User exists: {username}")


def seed_tasks():
    """Create sample tasks"""
    print("\nCreating sample tasks...")
    
    users = file_handler.read_json()['users']
    user_ids = [u['id'] for u in users if u['role'] == 'user']
    
    tasks = [
        ('Complete project proposal', 'high'),
        ('Review code changes', 'medium'),
        ('Update documentation', 'low'),
        ('Fix bug in dashboard', 'high'),
        ('Prepare presentation', 'medium'),
        ('Team meeting', 'high'),
        ('Email client updates', 'low'),
        ('Database optimization', 'medium'),
    ]
    
    for user_id in user_ids:
        for task_title, priority in tasks[:3]:
            task = file_handler.create_task(
                user_id=user_id,
                title=task_title,
                priority=priority,
                estimate_minutes=random.randint(30, 180)
            )
            if random.random() > 0.5:
                file_handler.update_task(task['id'], status='completed')
    
    print(f"   ✓ Created tasks for {len(user_ids)} users")


def seed_journal():
    """Create sample journal entries"""
    print("Creating sample journal entries...")
    
    users = file_handler.read_json()['users']
    user_ids = [u['id'] for u in users if u['role'] == 'user']
    
    entries = [
        "Today was productive. Completed 3 tasks and wrote significant progress on the project.",
        "Felt great today! Made good progress on learning new technologies.",
        "Had challenges but overcame them. Feeling accomplished.",
        "Good day overall. Meeting went well and got valuable feedback.",
        "Started implementing new features. Excited about the progress.",
    ]
    
    for user_id in user_ids:
        for i, entry in enumerate(entries[:2]):
            file_handler.create_journal_entry(
                user_id=user_id,
                content=entry,
                mood=random.randint(6, 10)
            )
    
    print(f"   ✓ Created journal entries for {len(user_ids)} users")


def seed_habits():
    """Create sample habit entries"""
    print("Creating sample habits...")
    
    users = file_handler.read_json()['users']
    user_ids = [u['id'] for u in users if u['role'] == 'user']
    
    habits = ['Morning Exercise', 'Meditation', 'Reading', 'Drinking Water']
    
    for user_id in user_ids:
        for habit in habits:
            # Create multiple entries for each habit
            for j in range(random.randint(3, 8)):
                file_handler.create_habit(user_id, habit)
    
    print(f"   ✓ Created habits for {len(user_ids)} users")


def seed_finance():
    """Create sample finance entries"""
    print("Creating sample finance entries...")
    
    users = file_handler.read_json()['users']
    user_ids = [u['id'] for u in users if u['role'] == 'user']
    
    categories = ['food', 'transport', 'entertainment', 'utilities', 'healthcare']
    
    for user_id in user_ids:
        for _ in range(random.randint(5, 15)):
            file_handler.create_finance_entry(
                user_id=user_id,
                amount=round(random.uniform(50, 500), 2),
                category=random.choice(categories),
                note=f"Sample transaction"
            )
    
    print(f"   ✓ Created finance entries for {len(user_ids)} users")


def seed_mood():
    """Create sample mood entries"""
    print("Creating sample mood entries...")
    
    users = file_handler.read_json()['users']
    user_ids = [u['id'] for u in users if u['role'] == 'user']
    
    for user_id in user_ids:
        for _ in range(random.randint(5, 10)):
            file_handler.create_mood_entry(
                user_id=user_id,
                mood_value=random.randint(1, 10),
                note="Sample mood entry"
            )
    
    print(f"   ✓ Created mood entries for {len(user_ids)} users")


def seed_focus():
    """Create sample focus sessions"""
    print("Creating sample focus sessions...")
    
    users = file_handler.read_json()['users']
    user_ids = [u['id'] for u in users if u['role'] == 'user']
    
    durations = [15, 25, 45, 60, 90]
    
    for user_id in user_ids:
        for _ in range(random.randint(5, 15)):
            file_handler.create_focus_session(
                user_id=user_id,
                minutes=random.choice(durations)
            )
    
    print(f"   ✓ Created focus sessions for {len(user_ids)} users")


def main():
    """Run all seeds"""
    print("🌱 Seeding database...\n")
    
    seed_users()
    seed_tasks()
    seed_journal()
    seed_habits()
    seed_finance()
    seed_mood()
    seed_focus()
    
    print("\n✅ Database seeding complete!")
    print("\nYou can now login with:")
    print("  Username: john_doe")
    print("  Password: password123")


if __name__ == '__main__':
    main()
