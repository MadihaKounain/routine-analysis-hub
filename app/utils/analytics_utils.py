from datetime import datetime, timedelta, timezone
from app.utils import file_handler


def calculate_task_completion_rate(user_id, days=7):
    """Calculate task completion rate for a user"""
    tasks = file_handler.get_user_tasks(user_id)
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    recent_tasks = [t for t in tasks if datetime.fromisoformat(t['created_at'].replace('Z', '+00:00')) > cutoff_date]
    
    if not recent_tasks:
        return 0
    
    completed = [t for t in recent_tasks if t['status'] == 'completed']
    return round((len(completed) / len(recent_tasks)) * 100) if recent_tasks else 0


def get_habit_streaks(user_id):
    """Get all habit streaks for a user"""
    habits = file_handler.get_user_habits(user_id)
    
    if not habits:
        return []
    
    # Get unique habit names
    habit_names = set(h['habit_name'] for h in habits)
    
    streaks = []
    for habit_name in habit_names:
        streak = file_handler.get_habit_streak(user_id, habit_name)
        total_completions = len([h for h in habits if h['habit_name'] == habit_name])
        streaks.append({
            'habit_name': habit_name,
            'streak': streak,
            'total_completions': total_completions
        })
    
    return streaks


def get_mood_analysis(user_id, days=7):
    """Analyze mood trends"""
    moods = file_handler.get_user_moods(user_id)
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    recent_moods = [m for m in moods if datetime.fromisoformat(m['created_at'].replace('Z', '+00:00')) > cutoff_date]
    
    if not recent_moods:
        return {'average': 0, 'count': 0, 'trend': []}
    
    mood_values = [m['mood'] for m in recent_moods if m['mood']]
    average = round(sum(mood_values) / len(mood_values), 2) if mood_values else 0
    
    # Group by date
    daily_moods = {}
    for mood in recent_moods:
        date = datetime.fromisoformat(mood['created_at'].replace('Z', '+00:00')).date()
        date_str = date.isoformat()
        if date_str not in daily_moods:
            daily_moods[date_str] = []
        if mood['mood']:
            daily_moods[date_str].append(mood['mood'])
    
    trend = []
    for date_str in sorted(daily_moods.keys()):
        avg_mood = round(sum(daily_moods[date_str]) / len(daily_moods[date_str]), 1)
        trend.append({'date': date_str, 'mood': avg_mood})
    
    return {
        'average': average,
        'count': len(recent_moods),
        'trend': trend
    }


def get_finance_summary(user_id, days=7):
    """Get finance summary for a user"""
    finances = file_handler.get_user_finances(user_id)
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    recent_finances = [f for f in finances if datetime.fromisoformat(f['created_at'].replace('Z', '+00:00')) > cutoff_date]
    
    total_spent = sum(f['amount'] for f in recent_finances)
    
    # Group by category
    by_category = {}
    for finance in recent_finances:
        category = finance['category']
        if category not in by_category:
            by_category[category] = 0
        by_category[category] += finance['amount']
    
    # Sort categories by amount spent
    categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'total_spent': round(total_spent, 2),
        'entry_count': len(recent_finances),
        'by_category': [{'category': cat, 'amount': round(amt, 2)} for cat, amt in categories]
    }


def calculate_productivity_score(user_id, days=7):
    """Calculate overall productivity score"""
    tasks = file_handler.get_user_tasks(user_id)
    focus_sessions = file_handler.get_user_focus_sessions(user_id)
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    recent_tasks = [t for t in tasks if datetime.fromisoformat(t['created_at'].replace('Z', '+00:00')) > cutoff_date]
    recent_focus = [f for f in focus_sessions if datetime.fromisoformat(f['created_at'].replace('Z', '+00:00')) > cutoff_date]
    
    # Calculate task completion score
    task_score = calculate_task_completion_rate(user_id, days)
    
    # Calculate focus score (total focus minutes / days)
    total_focus_minutes = sum(f['minutes'] for f in recent_focus)
    focus_score = min(40, (total_focus_minutes / (days * 60)) * 40) if days else 0
    
    # Habit consistency
    habits = file_handler.get_user_habits(user_id)
    recent_habits = [h for h in habits if datetime.fromisoformat(h['created_at'].replace('Z', '+00:00')) > cutoff_date]
    unique_habit_days = len(set(datetime.fromisoformat(h['created_at'].replace('Z', '+00:00')).date() for h in recent_habits))
    habit_score = min(20, (unique_habit_days / days) * 20) if days else 0
    
    # Total score: 50 (baseline) + task_score (40) + focus_score (40) + habit_score (20) - max 95
    total_score = round(50 + (task_score * 0.4) + (focus_score * 0.4) + (habit_score * 0.2))
    return min(95, max(40, total_score))


def get_daily_activity(user_id, days=7):
    """Get daily activity metrics"""
    tasks = file_handler.get_user_tasks(user_id)
    focus_sessions = file_handler.get_user_focus_sessions(user_id)
    habits = file_handler.get_user_habits(user_id)
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    activity_by_day = {}
    
    # Count tasks
    for task in tasks:
        task_date = datetime.fromisoformat(task['created_at'].replace('Z', '+00:00')).date()
        if task_date >= cutoff_date.date():
            date_str = task_date.isoformat()
            if date_str not in activity_by_day:
                activity_by_day[date_str] = 0
            activity_by_day[date_str] += 1
    
    # Count focus sessions
    for session in focus_sessions:
        session_date = datetime.fromisoformat(session['created_at'].replace('Z', '+00:00')).date()
        if session_date >= cutoff_date.date():
            date_str = session_date.isoformat()
            if date_str not in activity_by_day:
                activity_by_day[date_str] = 0
            activity_by_day[date_str] += 1
    
    # Count habit completions
    for habit in habits:
        habit_date = datetime.fromisoformat(habit['created_at'].replace('Z', '+00:00')).date()
        if habit_date >= cutoff_date.date():
            date_str = habit_date.isoformat()
            if date_str not in activity_by_day:
                activity_by_day[date_str] = 0
            activity_by_day[date_str] += 1
    
    # Build sorted activity array
    activity = []
    for i in range(days):
        date = (datetime.now(timezone.utc) - timedelta(days=days - i - 1)).date()
        date_str = date.isoformat()
        value = activity_by_day.get(date_str, 0)
        activity.append({'date': date_str, 'value': value})
    
    return activity


def get_user_analytics(user_id, days=7):
    """Get comprehensive analytics for a user"""
    tasks = file_handler.get_user_tasks(user_id)
    journal_entries = file_handler.get_user_journal(user_id)
    finances = file_handler.get_user_finances(user_id)
    focus_sessions = file_handler.get_user_focus_sessions(user_id)
    habits = file_handler.get_user_habits(user_id)
    moods = file_handler.get_user_moods(user_id)
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    recent_tasks = [t for t in tasks if datetime.fromisoformat(t['created_at'].replace('Z', '+00:00')) > cutoff_date]
    recent_journal = [j for j in journal_entries if datetime.fromisoformat(j['created_at'].replace('Z', '+00:00')) > cutoff_date]
    recent_finance = [f for f in finances if datetime.fromisoformat(f['created_at'].replace('Z', '+00:00')) > cutoff_date]
    
    completed_tasks = [t for t in recent_tasks if t['status'] == 'completed']
    pending_tasks = [t for t in recent_tasks if t['status'] == 'pending']
    
    total_spent = sum(f['amount'] for f in recent_finance)
    
    return {
        'summary': {
            'totalTasks': len(recent_tasks),
            'completedTasks': len(completed_tasks),
            'pendingTasks': len(pending_tasks),
            'productivityScore': calculate_productivity_score(user_id, days),
            'totalJournals': len(recent_journal),
            'totalExpenses': len(recent_finance),
            'totalSpent': round(total_spent, 2),
            'totalFocusMinutes': sum(f['minutes'] for f in file_handler.get_user_focus_sessions(user_id))
        },
        'dailyActivity': get_daily_activity(user_id, days),
        'moodTrend': get_mood_analysis(user_id, days),
        'habitStreaks': get_habit_streaks(user_id),
        'financeSummary': get_finance_summary(user_id, days)
    }


def get_all_users_analytics(days=7):
    """Get analytics for all users (admin)"""
    db = file_handler.read_json()
    users = db.get('users', [])
    
    all_analytics = []
    for user in users:
        if user['role'] == 'user':  # Skip admin users
            analytics = get_user_analytics(user['id'], days)
            all_analytics.append({
                'user_id': user['id'],
                'username': user['username'],
                'analytics': analytics
            })
    
    return all_analytics
