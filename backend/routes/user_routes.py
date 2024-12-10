from flask import Blueprint, request, jsonify
from backend.services.auth_service import AuthService
import logging
from ..logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/create-account', methods=['POST'])
def create_account():
    logger.info("Request to create account")
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Missing username or password")
        return jsonify({'error': 'Username and password are required'}), 400

    logger.info(f"Creating account for username: {username} with passoword: {password}")
    response, status_code = AuthService.create_user(username, password)
    logger.info(f"Account creation status code: {status_code}")
    return jsonify(response), status_code


@auth_blueprint.route('/login', methods=['POST'])
def login():
    logger.info("Request to login")
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning("Missing username or password")
        return jsonify({'error': 'Username and password are required'}), 400

    logger.info(f"Logging in for: {username}")
    response, status_code = AuthService.verify_user(username, password)
    logger.info(f"Login status code: {status_code}")
    return jsonify(response), status_code


@auth_blueprint.route('/update-password', methods=['POST'])
def update_password():
    logger.info("Request to update password")
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        logger.warning("Missing username, old password, or new password")
        return jsonify({'error': 'Username, old password, and new password are required'}), 400

    logger.info(f"Updating password for username: {username}")
    response, status_code = AuthService.update_password(username, old_password, new_password)
    logger.info(f"Update password status code: {status_code}")
    return jsonify(response), status_code
