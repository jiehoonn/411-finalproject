from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_cors import CORS

bp = Blueprint('auth', __name__)
CORS(bp)

@bp.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON payload:
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    """
    data = request.json
    
    # Validate required fields
    if not all(k in data for k in ["username", "email", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
        
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
        
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    try:
        # Create new user
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "username": user.username,
                "email": user.email,
                "balance": user.balance
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    Login a user.
    
    Expected JSON payload:
    {
        "username": "string",
        "password": "string"
    }
    """
    data = request.json
    
    # Validate required fields
    if not all(k in data for k in ["username", "password"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Verify password
    if user and user.check_password(data['password']):
        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user.username,
                "email": user.email,
                "balance": user.balance
            }
        }), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@bp.route('/api/auth/update-password', methods=['PUT'])
def update_password():
    """
    Update user password.
    
    Expected JSON payload:
    {
        "username": "string",
        "current_password": "string",
        "new_password": "string"
    }
    """
    data = request.json
    
    # Validate required fields
    if not all(k in data for k in ["username", "current_password", "new_password"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Verify current password
    if not user.check_password(data['current_password']):
        return jsonify({"error": "Current password is incorrect"}), 401
    
    try:
        # Update password
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({"message": "Password updated successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500