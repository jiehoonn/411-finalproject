from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime
from backend.database import db

class Stock(db.Model):
    """Stock model for tracking portfolio holdings"""
    
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # link stock to a user
    symbol = db.Column(String(10), nullable=False)
    shares = db.Column(Integer, nullable=False)
    purchase_price = db.Column(Float, nullable=False)  # store the purchase price for historical tracking
    purchase_date = db.Column(DateTime, default=datetime.utcnow)  # record the date of purchase
    
    # relationship to User
    user = db.relationship('User', back_populates='stocks')

    def to_dict(self):
        """Convert the stock instance to a dictionary"""
        return {
            'symbol': self.symbol,
            'shares': self.shares,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat()
        }

