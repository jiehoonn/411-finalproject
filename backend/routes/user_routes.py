from flask import Blueprint, request, jsonify
from backend.services.auth_service import AuthService

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/create-account', methods=['POST'])
def create_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    response, status_code = AuthService.create_user(username, password)
    return jsonify(response), status_code


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    response, status_code = AuthService.verify_user(username, password)
    return jsonify(response), status_code


@auth_blueprint.route('/update-password', methods=['POST'])
def update_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({'error': 'Username, old password, and new password are required'}), 400

    response, status_code = AuthService.update_password(username, old_password, new_password)
    return jsonify(response), status_code
