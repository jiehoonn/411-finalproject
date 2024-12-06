import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///stocktrading.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_SQLALCHEMY_TABLE = 'sessions'
