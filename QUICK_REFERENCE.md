# ⚡ QUICK REFERENCE GUIDE

## 🚀 START HERE

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create admin user
python scripts/create_admin.py

# 3. Run server
python run.py

# 4. Open browser
http://127.0.0.1:5000
```

---

## 📝 COMMON COMMANDS

#### Development
```bash
python run.py                      # Start dev server (debug mode)
python -m pytest                   # Run tests (if added)
python scripts/seed.py             # Populate test data
python scripts/create_admin.py     # Create admin user
```

#### Database
```bash
rm app/database/app.json           # Reset database
python scripts/seed.py             # Recreate with sample data
```

#### Configuration
```bash
cp .env.example .env               # Create .env from template
# Edit .env with your settings
```

#### Production
```bash
pip install gunicorn               # Install production server
gunicorn --config gunicorn_config.py run:app  # Run with gunicorn
```

---

## 🔑 LOGIN CREDENTIALS

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| User | john_doe | password123 |
| User | jane_smith | password123 |
| User | alex_kumar | password123 |

⚠️ **Change these in production!**

---

## 🌍 URLS to TEST

### User Pages
```
/ or /dashboard             Main dashboard
/register                   Create new account
/login                      User login
/tasks                      Task management
/journal                    Journal entries
/finance                    Expense tracking
/mood                       Mood logging
/habits                     Habit tracking
/focus                      Focus sessions
```

### Admin Pages
```
/admin/login                Admin login
/admin                      Admin dashboard
/admin/users                Users list
/admin/users/<user_id>      User details
```

### API Endpoints
```
/api/tasks                  Create/get tasks
/api/journal                Create/get journal
/api/finance                Create/get expenses
/api/mood                   Create/get moods
/api/habits                 Create/get habits
/api/focus                  Create/get focus sessions
/api/analytics              Get analytics data
```

---

## 📚 WHICH DOCUMENT FOR WHAT?

| Question | Document |
|----------|----------|
| "How do I start?" | README.md |
| "How is it structured?" | STRUCTURE.md |
| "How do I deploy?" | PRODUCTION_DEPLOYMENT.md |
| "How do I customize?" | IMPLEMENTATION_GUIDE.md |
| "What changed?" | IMPROVEMENTS.md |
| "Quick overview?" | PROJECT_STATUS.md |

---

## ⚙️ ENVIRONMENT VARIABLES

Create `.env` file:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
LOG_LEVEL=DEBUG
DATABASE_PATH=app/database/app.json
LOG_FILE=logs/app.log
HOST=127.0.0.1
PORT=5000
```

---

## 🔧 CONFIGURATION FILES

### config.py
- `DevelopmentConfig` - Debug on, verbose logging
- `TestingConfig` - Isolated database, testing mode
- `ProductionConfig` - Debug off, HTTPS required

### .env.example
- Template for environment variables
- Copy to `.env` and customize

### app/__init__.py
- App factory with config loading
- Logging setup
- Error handler registration
- Blueprint registration

---

## 📊 FILE ORGANIZATION

```
app/
  ├── routes/          ← Add new feature blueprints here
  ├── templates/       ← Add new HTML pages here
  ├── static/
  │   ├── css/        ← Modify styles here
  │   └── js/         ← Add JavaScript here
  ├── utils/          ← Add utilities here
  └── database/       ← JSON database created here
  
scripts/              ← Helper scripts
  ├── create_admin.py  ← Create admin user
  └── seed.py         ← Populate test data

config.py            ← Configuration
.env                 ← Environment variables
run.py               ← Entry point
```

---

## 🛡️ SECURITY CHECKLIST

- [ ] Change `SECRET_KEY` in config
- [ ] Update admin password
- [ ] Enable HTTPS in production
- [ ] Set `FLASK_ENV=production`
- [ ] Use Gunicorn (not Flask dev server)
- [ ] Set up log monitoring
- [ ] Configure backups
- [ ] Enable rate limiting (optional)

---

## 🐛 QUICK TROUBLESHOOT

| Problem | Solution |
|---------|----------|
| App won't start | `pip install -r requirements.txt` |
| Port in use | Change `PORT` in `.env` |
| Database error | Delete `app/database/app.json` and reseed |
| Logging not working | Create `logs/` directory manually |
| 404 errors | Check route spelling and decorators |
| Login fails | Check credentials or reseed database |

---

## 📈 PERFORMANCE TIPS

```python
# Cache frequently accessed data
@app.route('/api/analytics')
def get_analytics():
    # Add caching here for production
    return json.dumps(calculate_analytics())

# Use pagination for large datasets
@app.route('/api/users?page=1')
def get_users_paginated():
    pass
```

---

## 🔄 DEPLOYMENT QUICK STEPS

```bash
# 1. Set up production config
export FLASK_ENV=production
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 2. Install production dependencies
pip install -r requirements.txt
pip install gunicorn

# 3. Initialize admin
python scripts/create_admin.py

# 4. Create systemd service
sudo cp deployment/flask-app.service /etc/systemd/system/

# 5. Start service
sudo systemctl start flask-app

# 6. Set up Nginx
sudo cp deployment/nginx.conf /etc/nginx/sites-available/

# 7. Enable SSL
sudo certbot certonly --nginx -d yourdomain.com

# 8. Start Nginx
sudo systemctl start nginx
```

---

## 📝 FREQUENT TASKS

### Add New Route
```python
# In app/routes/myfeature.py
from flask import Blueprint, render_template

myfeature_bp = Blueprint('myfeature', __name__)

@myfeature_bp.route('/myfeature')
def my_feature():
    return render_template('myfeature.html')

# In app/__init__.py
app.register_blueprint(myfeature_bp)
```

### Add New Template
```html
<!-- In app/templates/myfeature.html -->
{% extends "base.html" %}

{% block title %}My Feature{% endblock %}

{% block content %}
<div class="container">
    <h1>My Feature</h1>
</div>
{% endblock %}
```

### Add CSS Class
```css
/* In app/static/css/style.css */
.my-class {
    color: blue;
    padding: 10px;
}
```

### Add Error Handler
```python
# In app/utils/errors.py
@app.errorhandler(418)  # I'm a teapot :)
def teapot_error(error):
    return render_template('errors/418.html'), 418
```

---

## 📊 ANALYTICS CALCULATIONS

```
Productivity Score = 40-95
  = Base(50) + TaskCompletion(40) + FocusTime(40) + Habits(20)

Task Completion Rate = Completed/Total * 100

Habit Streak = Consecutive days with completions

Mood Analysis = Average, min, max of 1-10 scale

Finance Summary = Total spent, grouped by category
```

---

## 🔗 URLS MAPPING

```
/                          → dashboard.index()
/register                  → auth.register()
/login                     → auth.login()
/logout                    → auth.logout()
/tasks                     → tasks.index()
/api/tasks                 → tasks.create_task()
/admin/login               → admin.admin_login()
/admin                     → admin.dashboard()
/admin/users               → admin.users_list()
/admin/users/<id>          → admin.user_detail()
```

---

## 💾 DATA MODELS

```python
User: id, username, email, password_hash, created_at, role
Task: id, user_id, title, priority, status, due_date
Habit: id, user_id, name, frequency, completions
Journal: id, user_id, content, mood, word_count
Finance: id, user_id, amount, category, description
Mood: id, user_id, mood (1-10), notes, created_at
Focus: id, user_id, duration (minutes), created_at
```

---

## 🎯 NEXT QUICK WINS

1. **Add Tests**
   ```bash
   pip install pytest
   # Create tests/test_routes.py
   pytest tests/
   ```

2. **Add Email Support**
   ```bash
   pip install flask-mail
   # Configure in config.py
   ```

3. **Add Database Migrations**
   ```bash
   pip install flask-migrate
   flask db init
   flask db migrate
   ```

4. **Add API Documentation**
   ```bash
   pip install flask-swagger
   # Auto-generate API docs
   ```

5. **Add Rate Limiting**
   ```bash
   pip install flask-limiter
   # Add to decorators
   ```

---

## 🚀 PERFORMANCE CHECKLIST

- [ ] Enable caching (Redis)
- [ ] Add pagination for large datasets
- [ ] Minify CSS and JavaScript
- [ ] Enable gzip compression
- [ ] Optimize database queries
- [ ] Use CDN for static files
- [ ] Monitor error rates
- [ ] Set up APM (Application Performance Monitoring)

---

## 🆘 COMMON ERRORS & FIXES

```
❌ SQLAlchemy Import Error
→ pip install sqlalchemy

❌ Jinja2 Template Not Found
→ Check app/templates/ folder structure

❌ Module Not Found
→ Check __init__.py in package folder

❌ CORS Errors
→ pip install flask-cors
   app.config['CORS_ORIGINS'] = ['*']

❌ Session Cookie Error
→ Check SECRET_KEY is set in production

❌ Database Locked
→ Make sure only one process accesses app.json
```

---

## 💡 PRO TIPS

1. **Use `.env` locally, environment variables in production**
2. **Keep SECRET_KEY strong** (32+ characters)
3. **Monitor logs** regularly for errors
4. **Backup database** before updates
5. **Test in production config** before deploying
6. **Enable HTTPS** in production (not optional)
7. **Use Gunicorn** (not Flask dev server)
8. **Set up monitoring** for uptime

---

## 📞 SUPPORT

- **Installation Help** → Check GETTING_STARTED.md
- **Architecture Questions** → Read STRUCTURE.md
- **Deployment Issues** → See PRODUCTION_DEPLOYMENT.md
- **Code Examples** → Check IMPLEMENTATION_GUIDE.md
- **Configuration** → Review config.py and .env.example

---

**Start:** `python run.py`  
**Access:** http://127.0.0.1:5000  
**Login:** admin / admin123  

Happy coding! 🚀
