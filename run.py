#!/usr/bin/env python
"""Run the Flask application with environment configuration"""

import os
import sys
import logging

# Add current directory to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Load environment variables from .env file BEFORE importing app
try:
    from dotenv import load_dotenv
    env_file = os.path.join(project_root, '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print(f"✓ Loaded environment from {env_file}")
    else:
        print(f"⚠ .env file not found at {env_file}")
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables.")

from app import create_app
from config import get_config

if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    config = get_config(env)
    
    # Create app
    app = create_app(env)
    
    # Get host and port from environment or config
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = app.debug
    
    print("\n" + "="*60)
    print("Starting Routine Analytics Hub")
    print("="*60)
    print(f"Environment: {env.upper()}")
    print(f"Debug Mode: {'ON' if debug else 'OFF'}")
    print(f"Open: http://{host}:{port}")
    print(f"Logs: {config.LOG_FILE}")
    print("Press CTRL+C to stop")
    print("="*60 + "\n")
    
    # Run the application
    try:
        app.run(debug=debug, host=host, port=port, use_reloader=debug)
    except KeyboardInterrupt:
        print("\nShutting down...\n")
        sys.exit(0)
