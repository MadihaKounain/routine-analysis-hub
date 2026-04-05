# 📁 Project Structure Guide

## Directory Tree

```
routine-analytics-hub/
├── app/                              # Main Flask application package
│   ├── __init__.py                  # App factory with logging & error handlers
│   ├── main.py                      # Alternative entry point
│   ├── routes/                      # URL route modules (blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py                  # Authentication routes (register, login, logout)
│   │   ├── admin.py                 # Admin panel routes
│   │   ├── dashboard.py             # Main dashboard with analytics
│   │   ├── tasks.py                 # Task management CRUD
│   │   ├── journal.py               # Journal entries
│   │   ├── finance.py               # Finance tracking
│   │   ├── mood.py                  # Mood logging
│   │   ├── habits.py                # Habit tracking
│   │   └── focus.py                 # Focus session logging
│   ├── templates/                   # Jinja2 HTML templates
│   │   ├── base.html                # Master layout template
│   │   ├── errors/                  # Error pages
│   │   │   ├── 400.html             # Bad Request
│   │   │   ├── 401.html             # Unauthorized
│   │   │   ├── 403.html             # Forbidden
│   │   │   ├── 404.html             # Not Found
│   │   │   └── 500.html             # Internal Server Error
│   │   ├── auth/                    # Authentication templates
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── admin_login.html
│   │   ├── dashboard.html           # Main dashboard
│   │   ├── tasks.html               # Tasks page
│   │   ├── journal.html             # Journal page
│   │   ├── finance.html             # Finance page
│   │   ├── mood.html                # Mood page
│   │   ├── habits.html              # Habits page
│   │   ├── focus.html               # Focus page
│   │   ├── admin/                   # Admin panel templates
│   │   │   ├── dashboard.html
│   │   │   ├── users_list.html
│   │   │   ├── user_detail.html
│   │   │   └── user_not_found.html
│   │   └── __init__.py
│   ├── static/                      # CSS, JavaScript, images
│   │   ├── css/
│   │   │   └── style.css            # Tailwind-like CSS framework (2000+ lines)
│   │   ├── js/
│   │   │   └── main.js              # Vanilla JavaScript utilities
│   │   └── images/                  # Images and icons
│   ├── utils/                       # Utility modules
│   │   ├── __init__.py
│   │   ├── file_handler.py          # JSON database abstraction & CRUD operations
│   │   ├── auth_utils.py            # Password hashing, token management
│   │   ├── analytics_utils.py       # All analytics calculations
│   │   ├── decorators.py            # Custom Flask decorators (auth, logging, error handling)
│   │   ├── errors.py                # Error handler registration
│   │   ├── logger.py                # Logging configuration
│   │   ├── models.py                # Data model documentation
│   │   └── __pycache__/
│   ├── database/                    # Database files
│   │   ├── app.json                 # Main data store (auto-created)
│   │   └── .gitignore
│   └── __pycache__/
│
├── config.py                        # Configuration management for different environments
├── run.py                           # Main entry point to start the application
├── requirements.txt                 # Python package dependencies
├── .env.example                     # Environment variables template
├── .env                             # Local environment variables (create from .env.example)
├── .gitignore                       # Git ignore patterns
│
├── scripts/                         # Setup and utility scripts
│   ├── create_admin.py              # Create initial admin user
│   └── seed.py                      # Populate database with sample data
│
├── logs/                            # Application logs (created at runtime)
│   └── app.log                      # Main application log file
│
├── tests/                           # Test suite (optional, for future expansion)
│   └── test_db.json                 # Test database
│
└── docs/                            # Documentation files
    ├── README.md                    # Quick start guide
    ├── GETTING_STARTED.md           # Complete getting started guide
    ├── IMPLEMENTATION_GUIDE.md      # Technical architecture details
    ├── PROJECT_SUMMARY.md           # Project overview
    ├── FILE_TREE.md                 # File structure visualization
    ├── STRUCTURE.md                 # This file - project organization guide
    └── PRODUCTION_DEPLOYMENT.md     # Production deployment guide
```

---

## Module Breakdown

### 🔐 Authentication System (`app/utils/auth_utils.py`)
- **Purpose**: Password hashing and security token management
- **Key Functions**:
  - `hash_password(password)` - PBKDF2 hashing with 100k iterations
  - `verify_password(password, hash)` - Constant-time comparison
  - `sign_admin_token(user_id, username)` - Creates secure admin tokens
  - `verify_admin_token(token)` - Validates admin tokens with expiration

### 💾 Database Layer (`app/utils/file_handler.py`)
- **Purpose**: JSON database abstraction with CRUD operations
- **Features**:
  - Auto-initialization of database
  - Auto-incrementing ID generation
  - User management (create, read, search)
  - Task operations (CRUD)
  - Habit tracking with streak calculations
  - Journal entry storage
  - Finance entry management
  - Mood logging
  - Focus session logging
- **Data Format**: JSON with 7 collections (users, tasks, habits, journal, finance, mood, focus)

### 📊 Analytics Engine (`app/utils/analytics_utils.py`)
- **Purpose**: Calculate all analytics metrics
- **Key Calculations**:
  - Task completion rate
  - Habit streaks (consecutive days)
  - Mood analysis (average, trends)
  - Finance summary (total, by category)
  - Productivity score (40-95 scale)
  - Daily activity aggregation
  - User analytics compilation
- **Admin Functions**: System-wide analytics across all users

### 🎨 Decorators (`app/utils/decorators.py`)
- **Purpose**: Reusable Flask decorators for routes
- **Decorators**:
  - `@required_login` - Enforce authentication
  - `@required_admin` - Enforce admin role
  - `@log_request` - Log all requests
  - `@handle_json_errors` - Handle JSON API errors

### ⚙️ Error Handling (`app/utils/errors.py`)
- **Purpose**: Register error handlers with Flask
- **Handlers**: 400, 401, 403, 404, 500 with JSON/HTML responses
- **Features**: Proper logging, request type detection

### 📝 Logging (`app/utils/logger.py`)
- **Purpose**: Centralized logging configuration
- **Features**:
  - File rotation (max 10MB, 10 backups)
  - Console and file output
  - Environment-specific log levels
  - Formatted timestamps and module info

### 🛣️ Routes (`app/routes/`)
9 Flask blueprints handling different features:
- **auth.py** - Register, login, logout, admin access
- **dashboard.py** - Main dashboard & analytics
- **tasks.py** - Task CRUD operations
- **journal.py** - Journal entry management
- **finance.py** - Expense tracking
- **mood.py** - Mood logging
- **habits.py** - Habit tracking
- **focus.py** - Focus session logging
- **admin.py** - Admin panel & user management

### 🎯 Configuration (`config.py`)
- **Purpose**: Environment-based configuration
- **Classes**:
  - `Config` - Base configuration (all environments)
  - `DevelopmentConfig` - Development settings (debug=True)
  - `TestingConfig` - Testing settings
  - `ProductionConfig` - Production settings (debug=False, HTTPS)
- **Features**: Environment variable support, credential validation

---

## Data Flow

### User Registration Flow
```
register.html (form)
    ↓
routes/auth.py → register()
    ↓
auth_utils.py → hash_password()
    ↓
file_handler.py → create_user()
    ↓
app/database/app.json (wrote user)
```

### Task Creation Flow
```
tasks.html (form)
    ↓
routes/tasks.py → create_task()
    ↓
@required_login decorator
    ↓
file_handler.py → create_task()
    ↓
app/database/app.json (wrote task)
```

### Analytics Display Flow
```
dashboard.html (page load)
    ↓
routes/dashboard.py → index()
    ↓
analytics_utils.py → get_user_analytics()
    ↓
Multiple calculations:
  - Task completion rate
  - Habit streaks
  - Mood analysis
  - Finance summary
  - Productivity score
    ↓
render_template with analytics data
```

### Admin Panel Flow
```
admin_login.html (form)
    ↓
routes/admin.py → admin_login()
    ↓
auth_utils.py → verify_admin_token()
    ↓
Session stored, set role='admin'
    ↓
admin/dashboard.html (admin-only template)
    ↓
@required_admin decorator on admin routes
```

---

## Configuration Management

### Environment Variables (`.env` file)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
SESSION_COOKIE_SECURE=False
DATABASE_PATH=app/database/app.json
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log
HOST=127.0.0.1
PORT=5000
```

### Config Classes
- **DevelopmentConfig**: Debug=True, no HTTPS required, verbose logging
- **ProductionConfig**: Debug=False, HTTPS required, minimal logging, strong SECRET_KEY required
- **TestingConfig**: Test database path, CSRF disabled

### Loading Configuration
```python
from config import get_config
config = get_config('development')  # or os.getenv('FLASK_ENV')
```

---

## Security Features

✅ **Password Security**
- PBKDF2 hashing with 100,000 iterations
- Constant-time comparison (prevents timing attacks)

✅ **Session Management**
- HTTP-only cookies (JavaScript cannot access)
- SameSite=Lax (CSRF protection)
- Secure flag in production (HTTPS only)

✅ **Authentication**
- Login required via `@required_login` decorator
- Admin verification via `@required_admin` decorator
- Token-based admin access

✅ **Error Handling**
- No sensitive data in error messages
- Proper HTTP status codes
- Logged errors with full stack trace

✅ **Input Validation**
- Type checking in database operations
- Status/priority validation in routes
- Mood scale validation (1-10)

---

## Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Enable `SESSION_COOKIE_SECURE=True` (requires HTTPS)
- [ ] Generate SSL certificates
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy for app.json
- [ ] Set up log rotation
- [ ] Enable rate limiting
- [ ] Implement CSRF protection
- [ ] Regular security audits
- [ ] Update dependencies regularly

---

## Development Workflow

### 1. Setup
```bash
pip install -r requirements.txt
python scripts/create_admin.py
python scripts/seed.py
```

### 2. Development
```bash
# Copy .env.example to .env and customize
cp .env.example .env

# Run development server
python run.py

# Open browser
http://127.0.0.1:5000
```

### 3. Testing
```bash
# Test credentials from seed.py
Username: john_doe
Password: password123

# Admin
Username: admin
Password: admin123
```

### 4. Customization
- **Add new feature**: Create new blueprint in `app/routes/`
- **Add new template**: Create HTML in `app/templates/`
- **Update analytics**: Modify `app/utils/analytics_utils.py`
- **Add validation**: Enhance `app/utils/decorators.py`

---

## File Organization Best Practices

✅ **Routes** are organized by feature (tasks.py, journal.py, etc)
✅ **Templates** mirror route structure with subdirectories
✅ **Utilities** are separated by concern (auth, analytics, database)
✅ **Decorators** are centralized for reuse across routes
✅ **Configuration** is centralized and environment-aware
✅ **Logging** is set up globally at app startup
✅ **Error Handling** is registered centrally with Flask

---

## Performance Considerations

### Current (Development)
- **File-based database** suitable for <100 users
- **Synchronous requests** via Flask development server
- **Template rendering** server-side (no SPA overhead)

### Optimization Opportunities
- **Caching**: Add Redis for analytics calculations
- **Database**: Migrate to PostgreSQL for scaling
- **Server**: Use Gunicorn/uWSGI for production
- **Frontend**: Add CSS/JS minification
- **API**: Add response pagination and filtering
- **Async**: Use Celery for long-running tasks

---

## Troubleshooting

### Application won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Check imports
python -c "from app import create_app"

# Check dependencies
pip install -r requirements.txt
```

### Database issues
```bash
# Reset database
rm app/database/app.json
python scripts/seed.py
```

### Logging not working
```bash
# Check logs directory
ls logs/

# Check log level
# In .env: LOG_LEVEL=DEBUG
```

---

## Next Steps

1. ✅ Understand the current structure (this document)
2. 📝 Review IMPLEMENTATION_GUIDE.md for technical details
3. 🚀 Review PRODUCTION_DEPLOYMENT.md for deployment guide
4. 📊 Explore the routes and understand data flow
5. 🧪 Add tests if needed
6. 🚢 Deploy to production when ready

