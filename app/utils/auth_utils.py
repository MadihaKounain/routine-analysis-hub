import hashlib
import hmac
from datetime import datetime, timedelta
import json
import base64

# Admin session secret (should be in environment variable in production)
ADMIN_SESSION_SECRET = "change-this-secret"
ADMIN_SESSION_HOURS = 12


def hash_password(password):
    """Hash a password using PBKDF2"""
    salt = hashlib.sha256(b'salt-routine-hub').digest()
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.b64encode(pwd_hash).decode()


def verify_password(password, password_hash):
    """Verify a password against its hash"""
    try:
        return hash_password(password) == password_hash
    except Exception:
        return False


def sign_admin_token(user_id, username, role='admin'):
    """Sign an admin token"""
    exp = datetime.utcnow() + timedelta(hours=ADMIN_SESSION_HOURS)
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': int(exp.timestamp() * 1000)
    }
    
    # Create token with HMAC signature
    data = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    signature = hmac.new(
        ADMIN_SESSION_SECRET.encode(),
        data.encode(),
        digestmod=hashlib.sha256
    ).digest()
    signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    return f"{data}.{signature}"


def verify_admin_token(token):
    """Verify an admin token"""
    try:
        if not token or '.' not in token:
            return None
        
        data, signature = token.split('.')
        
        # Verify signature
        expected_sig = hmac.new(
            ADMIN_SESSION_SECRET.encode(),
            data.encode(),
            digestmod=hashlib.sha256
        ).digest()
        expected_sig = base64.urlsafe_b64encode(expected_sig).decode().rstrip('=')
        
        if not hmac.compare_digest(signature, expected_sig):
            return None
        
        # Decode payload
        payload = json.loads(base64.urlsafe_b64decode(data + '==').decode())
        
        # Check expiration
        if datetime.utcnow().timestamp() * 1000 > payload.get('exp', 0):
            return None
        
        if payload.get('role') != 'admin':
            return None
        
        return payload
    except Exception:
        return None
