# Routine Analytics Hub - Flask Version

A complete Flask-based rebuild of the Routine Analytics Hub with Jinja2 templates, vanilla JavaScript, and JSON file storage.

## Features

✅ **User Authentication** - Registration, login, session management
✅ **AI Wellness Coach** - Chat with AI-powered Gemini for personalized mental health support
✅ **Task Management** - Create, edit, track, complete tasks
✅ **Journal Entries** - Write reflections with mood tracking
✅ **Finance Tracking** - Track expenses by category
✅ **Mood Logging** - Daily mood tracking (1-10 scale)
✅ **Habits** - Track habits with streak calculations
✅ **Focus Sessions** - Log focus/Pomodoro sessions
✅ **Dashboard** - Real-time analytics and charts
✅ **Admin Panel** - View all users and their analytics

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API (For AI Chatbot)

The AI Wellness Coach requires a Google Gemini API key:

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `.env` file in project root with:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. See [GEMINI_SETUP.md](GEMINI_SETUP.md) for detailed instructions

### 3. Create Admin User

```bash
python scripts/create_admin.py
```

Admin login:
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

### 4. Seed Sample Data (Optional)

```bash
python scripts/seed.py
```

### 4. Run Application

```bash
python run.py
```

Then open: **http://127.0.0.1:5000**

## Default Users (After Seeding)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| john_doe | password123 | User |
| jane_smith | password123 | User |
| alex_kumar | password123 | User |

## Project Structure

```
routine-analytics-hub/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── main.py               # Main entry point
│   ├── routes/               # URL routes
│   │   ├── auth.py          # Login/Register
│   │   ├── dashboard.py     # Dashboard
│   │   ├── tasks.py         # Tasks management
│   │   ├── journal.py       # Journal entries
│   │   ├── finance.py       # Finance tracking
│   │   ├── mood.py          # Mood tracking
│   │   ├── habits.py        # Habits tracking
│   │   ├── focus.py         # Focus sessions
│   │   ├── chatbot.py       # AI Wellness Coach
│   │   └── admin.py         # Admin panel
│   ├── templates/            # Jinja2 templates
│   │   ├── base.html        # Base template
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Register page
│   │   ├── dashboard.html   # Dashboard page
│   │   ├── tasks.html       # Tasks page
│   │   ├── journal.html     # Journal page
│   │   ├── finance.html     # Finance page
│   │   ├── mood.html        # Mood page
│   │   ├── habits.html      # Habits page
│   │   ├── focus.html       # Focus page
│   │   ├── chatbot.html     # AI Chatbot
│   │   └── admin/           # Admin templates
│   │       ├── dashboard.html
│   │       ├── users_list.html
│   │       └── user_detail.html
│   ├── static/               # CSS & JavaScript
│   │   ├── css/style.css    # Main styles
│   │   └── js/main.js       # Main scripts
│   ├── utils/                # Utility modules
│   │   ├── file_handler.py  # JSON database
│   │   ├── auth_utils.py    # Auth helpers
│   │   └── analytics_utils.py # Analytics
│   └── database/
│       └── app.json          # JSON database
├── scripts/                  # Setup scripts
│   ├── create_admin.py      # Create admin user
│   └── seed.py              # Seed sample data
├── run.py                   # Main entry point
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## API Endpoints

### Authentication
- `GET /register` - Registration page
- `POST /register` - Register new user
- `GET /login` - Login page
- `POST /login` - User login
- `GET /admin/login` - Admin login page
- `POST /admin/login` - Admin authentication
- `GET /logout` - Logout

### Dashboard
- `GET /` or `/dashboard` - Main dashboard

### Tasks
- `GET /tasks` - Tasks page
- `POST /api/tasks` - Create task
- `PATCH /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

### Journal
- `GET /journal` - Journal page
- `POST /api/journal` - Create entry

### Finance
- `GET /finance` - Finance page
- `POST /api/finance` - Create expense

### Mood
- `GET /mood` - Mood page
- `POST /api/mood` - Log mood

### Habits
- `GET /habits` - Habits page
- `POST /api/habits` - Log habit

### Focus
- `GET /focus` - Focus page
- `POST /api/focus` - Log session

### Admin
- `GET /admin` - Admin dashboard
- `GET /admin/users` - Users list
- `GET /admin/users/<id>` - User details

## Technology Stack

- **Backend**: Flask 3.0
- **Database**: JSON file (app.json)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Charts**: Chart.js
- **Authentication**: Flask Sessions + Password hashing (PBKDF2)

## Features Implemented

### User Module
- ✅ Registration with validation
- ✅ Login/Logout
- ✅ Session management
- ✅ Password hashing

### Tasks Module
- ✅ Create/Edit/Delete tasks
- ✅ Priority levels (low, medium, high)
- ✅ Completion tracking
- ✅ Estimate vs actual time

### Journal Module
- ✅ Write entries
- ✅ Mood association (1-10 scale)
- ✅ Word count tracking
- ✅ Chronological display

### Finance Module
- ✅ Track expenses
- ✅ Categorize spending
- ✅ Summary by category
- ✅ Total spent tracking

### Mood Module
- ✅ Daily mood logging (1-10)
- ✅ Optional notes
- ✅ Emoji display
- ✅ Mood trends

### Habits Module
- ✅ Track habit completions
- ✅ Streak calculation
- ✅ Total completion count
- ✅ Multiple habits support

### Focus Module
- ✅ Log focus sessions
- ✅ Quick duration buttons
- ✅ Total focus time
- ✅ Session history

### Analytics
- ✅ Task completion rate
- ✅ Productivity score calculation
- ✅ Daily activity charts
- ✅ Mood trends
- ✅ Habit streaks
- ✅ Finance summary

### Admin Panel
- ✅ View all users
- ✅ Search users
- ✅ View individual user analytics
- ✅ System-wide statistics

## Environment Variables

Create a `.env` file (optional):

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

## Production Deployment

For production:

1. Set `FLASK_ENV=production`
2. Change `SECRET_KEY` to a strong random value
3. Set `SESSION_COOKIE_SECURE=True`
4. Use HTTPS
5. Consider using a proper database instead of JSON files
6. Run with a production WSGI server (Gunicorn, uWSGI, etc.)

## Troubleshooting

### Database not initializing
- Delete `app/database/app.json` and restart
- The database will be recreated automatically

### Session issues
- Clear browser cookies
- Restart the Flask server

### Static files not loading
- Check that Flask is serving from the correct static directory
- Clear browser cache

## License

MIT

## Support

For issues or questions, please refer to the original React/Node.js version for feature parity.
