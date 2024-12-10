from flask import Blueprint, request, jsonify
from backend.app.models import db, User, Portfolio
import requests

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/create-account', methods=['POST'])
def create_account():
    """
    Create a new user account.

    Handles the creation of a new user account by accepting a JSON payload
    containing `username`, `email`, and `password`. It ensures that all
    required fields are provided and that the username is unique. If the validation passes, a new
    user is added to the database with their password securely hashed.


    Returns:
        Response: A JSON response indicating the result of the operation.
            - Success: Returns a 201 status code with a success message.
            - Failure: Returns a 400 status code with an error message if any validation fails.

    Example:
    ```json
    {
        "username": "poop",
        "email": "poop@example.com",
        "password": "poop123"
    }
    ```

    Example Response (Success):
    ```json
    {
        "message": "Account created successfully"
    }
    ```

    Example Response (Failure)
    ```json
    {
        "error": "Missing fields"
    }
    ```
    or
    ```json
    {
        "error": "Username already exists"
    }
    ``` 
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'}), 201
