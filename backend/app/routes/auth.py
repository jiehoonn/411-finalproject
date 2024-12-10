from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_cors import CORS

bp = Blueprint('auth', __name__)
CORS(bp)

@bp.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register a new user.

    Handles user registration by accepting a JSON payload with the following fields:

    Args:
        None (data is retrieved from `request.json`):
            - username (str): The desired username of the user.
            - email (str): The email address of the user.
            - password (str): The desired password for the user.

    Returns:
        Response: A JSON response containing:
            - 201: On successful registration, the user's details.
            - 400: If required fields are missing or if the username or email already exists.
            - 500: If an internal server error occurs during the registration process.
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

    Handles user authentication by accepting a JSON payload with the following fields:

    Args:
        None (data is retrieved from `request.json`):
            - username (str): The username of the user.
            - password (str): The password of the user.

    Returns:
        Response: A JSON response containing:
            - 200: On successful authentication, the user's details.
            - 400: If required fields are missing in the request payload.
            - 401: If the provided credentials are invalid.
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
                "id": user.id,
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

    Allows a user to update their password by accepting a JSON payload with the following fields:

    Args:
        None (data is retrieved from `request.json`):
            - username (str): The username of the user.
            - current_password (str): The user's current password.
            - new_password (str): The new password to set for the user.

    Returns:
        Response: A JSON response containing:
            - 200: On successful password update, a success message.
            - 400: If required fields are missing in the request payload.
            - 401: If the current password is incorrect.
            - 404: If the specified user is not found.
            - 500: If an internal server error occurs during the password update process.
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
