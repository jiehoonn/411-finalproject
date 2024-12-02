from datetime import datetime, UTC
from sqlalchemy import Float, Integer, String, DateTime
from app import db

class Stock(db.Model):
    """Stock model for tracking portfolio holdings"""
    
    id = db.Column(Integer, primary_key=True)
    symbol = db.Column(String(10), nullable=False)
    shares = db.Column(Integer, nullable=False)
    purchase_price = db.Column(Float, nullable=False)
    purchase_date = db.Column(DateTime, default=datetime.now(UTC))
    
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'shares': self.shares,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat()
        }
