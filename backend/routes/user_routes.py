from flask import Blueprint, request, jsonify
from backend.app.models import db, User, Portfolio
import requests

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/create-account', methods=['POST'])
def create_account():
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

