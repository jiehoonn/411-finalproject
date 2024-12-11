from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_cors import CORS
import logging
from logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

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
    logger.info(f"Trying to register new user '{data.get('username')}'.")
    data = request.json

    if not all(k in data for k in ["username", "email", "password"]):
        logger.warning("Missing required fields for registration.")
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        logger.warning(f"Username: '{data['username']}' already exists.")
        return jsonify({"error": "Username already exists"}), 400

    if User.query.filter_by(email=data['email']).first():
        logger.warning(f"Email: '{data['email']}' already exists.")
        return jsonify({"error": "Email already exists"}), 400

    try:
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()
        logger.info(f"User '{user.username}' created successfully.")

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
        logger.error(f"Error during user registration: {str(e)}")
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
    logger.info(f"Trying to log in user '{data.get('username')}'.")
    data = request.json

    if not all(k in data for k in ["username", "password"]):
        logger.warning("Missing required fields for login.")
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        logger.info(f"Login successful for user '{user.username}'.")
        return jsonify({
            "message": "Login successful",
            "user": {
                "username": user.username,
                "email": user.email,
                "balance": user.balance
            }
        }), 200

    logger.warning("Invalid login credentials.")
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
    logger.info(f"Trying to update password for user '{data.get('username')}'.")
    data = request.json

    if not all(k in data for k in ["username", "current_password", "new_password"]):
        logger.warning("Missing required fields for update password.")
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user:
        logger.warning(f"User: '{data['username']}' not found.")
        return jsonify({"error": "User not found"}), 404

    if not user.check_password(data['current_password']):
        logger.warning("Current password is incorrect.")
        return jsonify({"error": "Current password is incorrect"}), 401

    try:
        user.set_password(data['new_password'])
        db.session.commit()
        logger.info(f"Password updated successfully for user '{user.username}'.")
        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during password update for user '{user.username}': {str(e)}")
        return jsonify({"error": str(e)}), 500
