from backend.database import db

class User(db.Model):
    """User model with relationship to stocks"""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    # relationship to Stock (one user can have many stocks)
    stocks = db.relationship('Stock', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"
