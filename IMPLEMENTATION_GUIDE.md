# IMPLEMENTATION GUIDE - Flask Version

## Overview

This document provides a comprehensive guide to the Flask-based translation of Routine Analytics Hub from Node.js/React to pure Flask with Jinja2 templates and vanilla JavaScript.

## Architecture Changes

### Original (Node.js + React)
```
Frontend: React (browser)
  ↓ (REST API)
Backend: Express.js
  ↓
Database: SQLite
```

### New (Flask)
```
Frontend: Jinja2 Templates + Vanilla JS (server-side rendering)
  ↓ (HTTP Requests)
Backend: Flask (Python)
  ↓
Database: JSON Files
```

## Key Differences

| Aspect | Original | New |
|--------|----------|-----|
| Frontend | React SPA | Server-side templates |
| Routing | React Router | Flask Blueprints |
| API | REST API (fetch) | Mixed HTML + JSON |
| Database | SQLite | JSON files |
| Auth | JWT Tokens | Flask Sessions |
| State | Redux/Context | Session + Database |

## Project Structure Details

```
routine-analytics-hub/
├── app/
│   ├── __init__.py
│   │   • Flask app factory function (create_app)
│   │   • Blueprint registration
│   │   • Configuration setup
│   │
│   ├── main.py
│   │   • Entry point - imports create_app
│   │   • Run Flask app directly
│   │
│   ├── routes/
│   │   ├── auth.py (Authentication)
│   │   │   • /register - User registration
│   │   │   • /login - User login
│   │   │   • /admin/login - Admin login
│   │   │   • /logout - Session cleanup
│   │   │   • required_login decorator for page protection
│   │   │   • required_admin decorator for admin areas
│   │   │
│   │   ├── dashboard.py (Dashboard)
│   │   │   • / - Main dashboard
│   │   │   • /dashboard - Same route
│   │   │   • /api/analytics - JSON analytics data
│   │   │
│   │   ├── tasks.py (Task Management)
│   │   │   • /tasks - Tasks list page
│   │   │   • POST /api/tasks - Create task
│   │   │   • PATCH /api/tasks/<id> - Update status
│   │   │   • DELETE /api/tasks/<id> - Delete task
│   │   │
│   │   ├── journal.py (Journal Entries)
│   │   │   • /journal - Journal page
│   │   │   • POST /api/journal - Create entry
│   │   │
│   │   ├── finance.py (Finance Tracking)
│   │   │   • /finance - Finance page
│   │   │   • POST /api/finance - Create expense
│   │   │
│   │   ├── mood.py (Mood Tracking)
│   │   │   • /mood - Mood page
│   │   │   • POST /api/mood - Log mood
│   │   │
│   │   ├── habits.py (Habits)
│   │   │   • /habits - Habits page
│   │   │   • POST /api/habits - Log habit
│   │   │
│   │   ├── focus.py (Focus Sessions)
│   │   │   • /focus - Focus page
│   │   │   • POST /api/focus - Log session
│   │   │
│   │   └── admin.py (Admin Panel)
│   │       • /admin - Admin dashboard
│   │       • /admin/users - Users list
│   │       • /admin/users/<id> - User details
│   │       • /api/admin/users - Users JSON
│   │       • /api/admin/analytics - Admin analytics
│   │
│   ├── templates/
│   │   ├── base.html
│   │   │   • Layout template with sidebar
│   │   │   • Header with username
│   │   │   • Navigation links
│   │   │   • Flash messages
│   │   │   • Template inheritance base
│   │   │
│   │   ├── login.html - User login page
│   │   ├── register.html - User registration page
│   │   ├── admin_login.html - Admin login page
│   │   │
│   │   ├── dashboard.html
│   │   │   • Stats grid (4 cards)
│   │   │   • Daily activity chart (Chart.js)
│   │   │   • Mood trend chart
│   │   │   • Habit streaks display
│   │   │
│   │   ├── tasks.html
│   │   │   • Task list with checkbox status
│   │   │   • Create task modal
│   │   │   • Priority badges
│   │   │   • Delete functionality
│   │   │
│   │   ├── journal.html
│   │   │   • Journal entries display
│   │   │   • Mood emoji display
│   │   │   • Create entry modal
│   │   │
│   │   ├── finance.html
│   │   │   • Finance summary cards
│   │   │   • Expense list
│   │   │   • Create expense modal
│   │   │
│   │   ├── mood.html
│   │   │   • Mood summary stats
│   │   │   • Mood history with emojis
│   │   │   • Create mood modal with slider
│   │   │
│   │   ├── habits.html
│   │   │   • Habit cards with streak display
│   │   │   • Create habit modal
│   │   │
│   │   ├── focus.html
│   │   │   • Focus summary stats
│   │   │   • Sessions list
│   │   │   • Quick duration buttons (15/25/45/60/90 min)
│   │   │
│   │   └── admin/
│   │       ├── dashboard.html - Admin overview
│   │       ├── users_list.html - Paginated users
│   │       ├── user_detail.html - User analytics
│   │       └── user_not_found.html - 404 page
│   │
│   ├── static/
│   │   ├── css/style.css
│   │   │   • Full Tailwind-like CSS framework
│   │   │   • Grid, flex, spacing utilities
│   │   │   • Color scheme
│   │   │   • Responsive design
│   │   │   • Form styling
│   │   │   • Button styles
│   │   │   • Modal styling
│   │   │
│   │   └── js/main.js
│   │       • Helper functions
│   │       • show/hide elements
│   │       • Toast notifications
│   │       • Date formatting
│   │       • API call helpers
│   │       • Form serialization
│   │
│   ├── utils/
│   │   ├── __init__.py - Package marker
│   │   │
│   │   ├── file_handler.py (Database abstraction)
│   │   │   • read_json() - Read entire database
│   │   │   • write_json(data) - Write to database
│   │   │   • get_next_id(collection) - Auto-increment
│   │   │   • User operations
│   │   │     - get_user_by_email()
│   │   │     - get_user_by_username()
│   │   │     - get_user_by_id()
│   │   │     - create_user()
│   │   │     - get_all_users()
│   │   │   • Task operations
│   │   │     - get_user_tasks()
│   │   │     - create_task()
│   │   │     - update_task()
│   │   │     - delete_task()
│   │   │   • Journal, Finance, Mood, Habits, Focus operations
│   │   │
│   │   ├── auth_utils.py (Authentication)
│   │   │   • hash_password(password) - PBKDF2 hashing
│   │   │   • verify_password(pwd, hash) - Compare
│   │   │   • sign_admin_token() - Create admin token
│   │   │   • verify_admin_token() - Validate token
│   │   │
│   │   └── analytics_utils.py (Analytics calculations)
│   │       • calculate_task_completion_rate()
│   │       • get_habit_streaks()
│   │       • get_mood_analysis()
│   │       • get_finance_summary()
│   │       • calculate_productivity_score()
│   │       • get_daily_activity()
│   │       • get_user_analytics() - Comprehensive stats
│   │       • get_all_users_analytics() - For admin
│   │
│   └── database/
│       └── app.json (Auto-created)
│           {
│             "users": [...],
│             "tasks": [...],
│             "habits": [...],
│             "journal": [...],
│             "finance": [...],
│             "mood": [...],
│             "focus": [...]
│           }
│
├── scripts/
│   ├── create_admin.py
│   │   • Creates default admin user
│   │   • Sets username: admin
│   │   • Sets password: admin123
│   │   • Should be run once on setup
│   │
│   └── seed.py
│       • Populates database with demo data
│       • Creates 3 sample users
│       • Adds tasks, journal, habits, etc.
│       • Optional - for testing/demo purposes
│
├── requirements.txt
│   • Flask 3.0.0
│   • Flask-Session 0.5.0
│   • Werkzeug 3.0.1
│
├── run.py - Main entry point
│
└── README.md - Quick start guide
```

## Database Schema (JSON)

```javascript
{
  "users": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "password_hash": "base64_encoded_pbkdf2_hash",
      "role": "user",
      "created_at": "2026-04-05T10:00:00.000Z"
    }
  ],
  
  "tasks": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Complete project",
      "status": "completed|pending|incomplete",
      "priority": "low|medium|high",
      "estimate_minutes": 120,
      "actual_minutes": 100,
      "created_at": "2026-04-05T09:00:00.000Z",
      "completed_at": "2026-04-05T11:00:00.000Z"
    }
  ],
  
  "habits": [
    {
      "id": 1,
      "user_id": 1,
      "habit_name": "Morning Exercise",
      "created_at": "2026-04-05T07:00:00.000Z"
    }
  ],
  
  "journal": [
    {
      "id": 1,
      "user_id": 1,
      "content": "Today was productive...",
      "mood": 8,
      "word_count": 42,
      "created_at": "2026-04-05T20:00:00.000Z"
    }
  ],
  
  "finance": [
    {
      "id": 1,
      "user_id": 1,
      "amount": 500.00,
      "category": "groceries",
      "note": "Weekly shopping",
      "created_at": "2026-04-05T15:30:00.000Z"
    }
  ],
  
  "mood": [
    {
      "id": 1,
      "user_id": 1,
      "mood": 7,
      "note": "Feeling good today",
      "created_at": "2026-04-05T18:00:00.000Z"
    }
  ],
  
  "focus": [
    {
      "id": 1,
      "user_id": 1,
      "minutes": 25,
      "created_at": "2026-04-05T14:00:00.000Z"
    }
  ]
}
```

## Session Management

### Login Flow
1. User submits form → POST /login
2. Validate credentials
3. Set session['user_id'] and session['username']
4. Redirect to dashboard

### Protected Routes
- Decorator `@required_login` checks `session['user_id']`
- Decorator `@required_admin` checks `session['is_admin']` + role='admin'

### Logout
- Clear session
- Redirect to login page

## Authentication

### Password Hashing
- Algorithm: PBKDF2 (Werkzeug standard)
- Salt: Fixed 'salt-routine-hub' (should be random in production)
- Iterations: 100,000

### Admin Token (for API)
- JWT-like format: `data.signature`
- Expires after 12 hours
- Used for admin API endpoints

## Frontend Interaction

### Server-Side Rendering
- Most pages render complete HTML
- Faster first load
- Better SEO

### Dynamic Features (JavaScript)
- Modal dialogs (show/hide)
- Form submission (AJAX)
- Chart rendering (Chart.js)
- DOM manipulation

### No Build Step
- Vanilla JavaScript (no Babel)
- Inline scripts in templates
- CSS utilities similar to Tailwind

## Analytics Calculations

### Productivity Score
```
Base: 50
+ Task Completion Rate × 0.4
+ Focus Sessions × 0.4
+ Habit Consistency × 0.2
= Score (clamped 40-95)
```

### Task Completion Rate
```
Completed Tasks / Total Tasks × 100
```

### Habit Streaks
```
Count consecutive days with habit completions
```

### Daily Activity
```
Count tasks + habit completions + focus sessions per day
```

## API Response Formats

### Task Creation
```json
{
  "id": 5,
  "user_id": 1,
  "title": "New Task",
  "status": "pending",
  "priority": "medium",
  "estimate_minutes": null,
  "actual_minutes": null,
  "created_at": "2026-04-05T10:30:00.000Z",
  "completed_at": null
}
```

### Analytics Response
```json
{
  "summary": {
    "totalTasks": 10,
    "completedTasks": 7,
    "pendingTasks": 2,
    "productivityScore": 75,
    "totalJournals": 5,
    "totalExpenses": 8,
    "totalSpent": 2500.50,
    "totalFocusMinutes": 270
  },
  "dailyActivity": [
    {"date": "2026-03-30", "value": 2},
    {"date": "2026-03-31", "value": 3}
  ],
  "moodTrend": {
    "average": 7.2,
    "count": 8,
    "trend": [
      {"date": "2026-03-30", "mood": 6.5},
      {"date": "2026-03-31", "mood": 8.0}
    ]
  },
  "habitStreaks": [
    {"habit_name": "Exercise", "streak": 5, "total_completions": 12}
  ],
  "financeSummary": {
    "total_spent": 2500.50,
    "entry_count": 8,
    "by_category": [
      {"category": "food", "amount": 1200.00}
    ]
  }
}
```

## URL Routing Map

### User Routes
```
GET  /                          → Dashboard
POST /register                  → Register user
GET  /login                     → Login page
POST /login                     → Process login
GET  /logout                    → Logout

GET  /tasks                     → Tasks page
POST /api/tasks                 → Create task
PATCH /api/tasks/<id>          → Update task
DELETE /api/tasks/<id>         → Delete task

GET  /journal                   → Journal page
POST /api/journal              → Create entry

GET  /finance                   → Finance page
POST /api/finance              → Create expense

GET  /mood                      → Mood page
POST /api/mood                 → Log mood

GET  /habits                    → Habits page
POST /api/habits               → Log habit

GET  /focus                     → Focus page
POST /api/focus                → Create session

GET  /api/analytics            → Analytics JSON
```

### Admin Routes
```
GET  /admin/login              → Admin login
POST /admin/login              → Process admin login

GET  /admin                     → Admin dashboard
GET  /admin/users              → Users list
GET  /admin/users/<id>         → User details

GET  /api/admin/users          → Users JSON
GET  /api/admin/analytics      → Admin analytics
```

## Feature Checklist

- [x] User registration & login
- [x] Admin authentication
- [x] Task management (CRUD)
- [x] Journal entries with mood
- [x] Finance tracking by category
- [x] Mood logging (1-10 scale)
- [x] Habit tracking with streaks
- [x] Focus sessions
- [x] Analytics dashboard with charts
- [x] Daily activity tracking
- [x] Admin panel with user search
- [x] User detail view with analytics
- [x] Session management
- [x] Password hashing
- [x] Responsive design

## Testing Credentials

After running `create_admin.py` and `seed.py`:

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Role: Admin

**Regular Users:**
- Username: `john_doe`
- Password: `password123`
- Username: `jane_smith`
- Password: `password123`
- Username: `alex_kumar`
- Password: `password123`

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Note: Chart.js requires modern browser with canvas support.

## Performance Considerations

- JSON file database suitable for small teams only
- For production, migrate to SQL database
- Consider caching analytics calculations
- Add rate limiting for login endpoints
- Use HTTPS in production

## Security Notes

- Change admin password immediately
- Never commit database file to version control
- Use environment variables for secrets
- Enable CSRF protection for forms (optional)
- Validate all user inputs (partially done)
- Use HTTPS in production
- Set secure session cookies in production
