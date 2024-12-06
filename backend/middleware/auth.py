from functools import wraps
from flask import session, jsonify, request
from backend.app.models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401
            
        request.user = user
        return f(*args, **kwargs)
    return decorated_function
