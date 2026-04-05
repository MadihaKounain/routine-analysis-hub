#!/usr/bin/env python
"""Create admin user"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils import file_handler, auth_utils

def create_admin():
    """Create an admin user"""
    print("Creating admin user...")
    
    # Check if admin already exists
    admin = file_handler.get_user_by_username('admin')
    if admin:
        print("Admin user already exists!")
        return
    
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'  # Change this in production!
    
    password_hash = auth_utils.hash_password(password)
    admin_user = file_handler.create_user(username, email, password_hash, role='admin')
    
    print(f"✅ Admin user created!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\n⚠️  IMPORTANT: Change the password in production!")
    print(f"   Admin ID: {admin_user['id']}")

if __name__ == '__main__':
    create_admin()
