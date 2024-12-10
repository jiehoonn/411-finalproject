from backend.models.user_model import User
from backend.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class AuthService:
    @staticmethod
    def create_user(username, password):
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 400

        salt = secrets.token_hex(32)
        hashed_password = generate_password_hash(password + salt)

        new_user = User(username=username, salt=salt, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Account created successfully'}, 201

    @staticmethod
    def verify_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'error': 'Invalid username or password'}, 401

        if check_password_hash(user.hashed_password, password + user.salt):
            return {'message': 'Login successful'}, 200
        else:
            return {'error': 'Invalid username or password'}, 401

    @staticmethod
    def update_password(username, old_password, new_password):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'error': 'Invalid username or password'}, 401

        if not check_password_hash(user.hashed_password, old_password + user.salt):
            return {'error': 'Invalid old password'}, 401

        new_salt = secrets.token_hex(32)
        new_hashed_password = generate_password_hash(new_password + new_salt)

        user.salt = new_salt
        user.hashed_password = new_hashed_password
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200



# import os
# import hashlib
# from flask import Blueprint, request, jsonify
# from backend.models.user import User
# from backend.database import db

# auth_blueprint = Blueprint('auth', __name__)

# # helper function to hash passwords
# def hash_password(password, salt):
#     return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

# @auth_blueprint.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'Username and password are required!'}), 400

#     # check if user already exists
#     if User.query.filter_by(username=username).first():
#         return jsonify({'message': 'User already exists!'}), 400

#     # generate salt and hash the password
#     salt = os.urandom(32).hex()
#     hashed_password = hash_password(password, salt)

#     # create and save the user
#     new_user = User(username=username, salt=salt, hashed_password=hashed_password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully!'}), 201

# @auth_blueprint.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'Username and password are required!'}), 400

#     # Fetch user from database
#     user = User.query.filter_by(username=username).first()
#     if not user:
#         return jsonify({'message': 'Invalid username or password!'}), 401

#     # Verify the password
#     hashed_password = hash_password(password, user.salt)
#     if hashed_password != user.hashed_password:
#         return jsonify({'message': 'Invalid username or password!'}), 401

#     return jsonify({'message': 'Login successful!'}), 200
