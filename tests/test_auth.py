import pytest
from flask import Flask
from backend.app.models import db, User
from backend.app.routes.auth import bp as auth_bp
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    db.init_app(app)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword123"
    }

##########################################################
# User Registration
##########################################################

def test_register_user_success(client, sample_user):
    """Test registering a new user successfully."""
    response = client.post('/api/auth/register', json=sample_user)
    assert response.status_code == 201, "User should be registered successfully."
    data = response.get_json()
    assert data['user']['username'] == sample_user['username'], "Username should match the input."
    assert data['user']['email'] == sample_user['email'], "Email should match the input."

def test_register_user_missing_fields(client):
    """Test registering a user with missing fields."""
    response = client.post('/api/auth/register', json={"username": "testuser"})
    assert response.status_code == 400, "Missing fields should result in a 400 error."
    data = response.get_json()
    assert "error" in data, "Error message should be returned."

def test_register_user_duplicate_username(client, sample_user):
    """Test registering a user with a duplicate username."""
    client.post('/api/auth/register', json=sample_user)
    response = client.post('/api/auth/register', json=sample_user)
    assert response.status_code == 400, "Duplicate username should result in a 400 error."
    data = response.get_json()
    assert "error" in data, "Error message should be returned."

##########################################################
# User Login
##########################################################

def test_login_success(client, sample_user):
    """Test logging in with valid credentials."""
    client.post('/api/auth/register', json=sample_user)
    response = client.post('/api/auth/login', json={"username": sample_user['username'], "password": sample_user['password']})
    assert response.status_code == 200, "Valid credentials should result in a successful login."
    data = response.get_json()
    assert data['user']['username'] == sample_user['username'], "Username should match the input."

def test_login_invalid_credentials(client, sample_user):
    """Test logging in with invalid credentials."""
    client.post('/api/auth/register', json=sample_user)
    response = client.post('/api/auth/login', json={"username": sample_user['username'], "password": "wrongpassword"})
    assert response.status_code == 401, "Invalid credentials should result in a 401 error."
    data = response.get_json()
    assert "error" in data, "Error message should be returned."

def test_login_nonexistent_user(client):
    """Test logging in with a non-existent user."""
    response = client.post('/api/auth/login', json={"username": "nonexistentuser", "password": "password"})
    assert response.status_code == 401, "Non-existent user should result in a 401 error."
    data = response.get_json()
    assert "error" in data, "Error message should be returned."

##########################################################
# Update Password
##########################################################

def test_update_password_success(client, sample_user):
    """Test updating the password for an existing user."""
    client.post('/api/auth/register', json=sample_user)
    response = client.put('/api/auth/update-password', json={
        "username": sample_user['username'],
        "current_password": sample_user['password'],
        "new_password": "newpassword456"
    })
    assert response.status_code == 200, "Password update should be successful."
    data = response.get_json()
    assert "message" in data, "Success message should be returned."

def test_update_password_incorrect_current_password(client, sample_user):
    """Test updating the password with an incorrect current password."""
    client.post('/api/auth/register', json=sample_user)
    response = client.put('/api/auth/update-password', json={
        "username": sample_user['username'],
        "current_password": "wrongpassword",
        "new_password": "newpassword456"
    })
    assert response.status_code == 401, "Incorrect current password should result in a 401 error."
    data = response.get_json()
    assert "error" in data, "Error message should be returned."

def test_update_password_user_not_found(client):
    """Test updating the password for a non-existent user."""
    response = client.put('/api/auth/update-password', json={
        "username": "nonexistentuser",
        "current_password": "password",
        "new_password": "newpassword456"
    })
    assert response.status_code == 404, "Non-existent user should result in a 404 error."
    data = response.get_json()
    assert "error" in data, "Error message should be returned."
