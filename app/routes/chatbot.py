from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from functools import wraps
from app.utils import file_handler
import os
import json
import requests
from difflib import SequenceMatcher

chatbot_bp = Blueprint('chatbot', __name__)

def chatbot_login_required(f):
    """Decorator to require login for chatbot"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def load_qa_database():
    """Load the local wellness Q&A database"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'app', 'database', 'wellness_qa.json')
        with open(db_path, 'r') as f:
            return json.load(f)
    except:
        return None

def find_best_match(user_message):
    """Find the best matching Q&A pair for user message using keyword matching"""
    qa_db = load_qa_database()
    if not qa_db:
        return None
    
    user_message_lower = user_message.lower()
    best_match = None
    best_score = 0
    
    for qa_pair in qa_db.get('qa_pairs', []):
        keywords = qa_pair.get('keywords', [])
        
        # Check how many keywords match
        keyword_matches = sum(1 for kw in keywords if kw in user_message_lower)
        
        if keyword_matches > 0:
            # Calculate score based on keyword matches and string similarity
            similarity_score = SequenceMatcher(None, user_message_lower, qa_pair.get('question', '').lower()).ratio()
            total_score = keyword_matches * 10 + (similarity_score * 100)
            
            if total_score > best_score:
                best_score = total_score
                best_match = qa_pair
    
    return best_match

@chatbot_bp.route('/chatbot')
@chatbot_login_required
def index():
    """AI Chatbot page"""
    return render_template('chatbot.html')

@chatbot_bp.route('/api/user-data')
@chatbot_login_required
def get_user_data():
    """Get user data for personalized AI responses"""
    user_id = session['user_id']
    
    # Get latest mood
    moods = file_handler.get_user_moods(user_id)
    latest_mood = moods[0]['mood'] if moods else 5
    
    # Get recent activity
    tasks = file_handler.get_user_tasks(user_id)
    recent_tasks = len([t for t in tasks if t.get('completed', False)])
    
    return jsonify({
        'latestMood': latest_mood,
        'recentTasksCompleted': recent_tasks,
        'totalTasks': len(tasks)
    })

@chatbot_bp.route('/api/chat', methods=['POST'])
@chatbot_login_required
def chat():
    """AI chat endpoint - uses local Q&A database (no API key required)"""
    user_id = session['user_id']
    data = request.get_json(silent=True) or {}
    user_message = (data.get('message') or '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        # Get user context for personalization
        moods = file_handler.get_user_moods(user_id)
        latest_mood = moods[0]['mood'] if moods else 5
        tasks = file_handler.get_user_tasks(user_id)
        
        # Find best matching Q&A pair
        matched_qa = find_best_match(user_message)
        
        if matched_qa:
            ai_response = matched_qa.get('answer', 'I appreciate your question. While I don\'t have a specific answer, I encourage you to think deeply about what matters most to you and reach out for support if needed.')
        else:
            # Generic response if no match found
            ai_response = f"""I appreciate your question about {user_message[:30]}...

While I don't have a specific answer to that, here are some general suggestions:

1. **Reach out to others**: Talk to friends, family, or a professional who might have relevant experience.

2. **Research**: Look for credible resources online or books on your specific topic.

3. **Professional support**: For wellness concerns, consider speaking with a therapist, counselor, or healthcare provider.

4. **Reflect**: Sometimes the best answers come from within through journaling or meditation.

5. **Be patient**: Not everything has an immediate answer, and that's okay.

I'm here to help with many wellness topics. Feel free to ask about mood, stress, sleep, productivity, goals, exercise, relationships, or other wellbeing-related topics!"""
        
        return jsonify({
            'response': ai_response,
            'userMood': latest_mood,
            'taskCount': len(tasks),
            'matched': matched_qa is not None
        }), 200
        
    except Exception as e:
        from app.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error in chat endpoint: {type(e).__name__} - {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Error: {str(e)}'}), 500

