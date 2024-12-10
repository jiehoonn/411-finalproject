from typing import List, Dict
from models.stock import Stock
from services.alpha_vantage import AlphaVantageService

class PortfolioService:
    def __init__(self):
        self.alpha_vantage = AlphaVantageService()
    
    def calculate_holding_value(self, stock: Stock) -> float:
        """Calculate current value of a stock holding
        
        Args:
            stock: Stock model instance
            
        Returns:
            Current value of the holding based on latest price
        """
        quote = self.alpha_vantage.get_stock_quote(stock.symbol)
        current_price = float(quote['Global Quote']['05. price'])
        return current_price * stock.shares

from backend.database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stock_symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('portfolio', lazy=True))

    def __repr__(self):
        return f"<Portfolio {self.stock_symbol}, Shares: {self.shares}>"

# services/portfolio.py
from services.alpha_vantage import AlphaVantageService
from models.stock import Stock

class PortfolioService:
    def __init__(self):
        self.alpha_vantage = AlphaVantageService()

    def calculate_holding_value(self, stock: Stock) -> float:
        """Calculate current value of a stock holding based on the latest market price."""
        quote = self.alpha_vantage.get_stock_quote(stock.symbol)
        current_price = float(quote['Global Quote']['05. price'])
        return current_price * stock.shares
