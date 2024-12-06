from models.stock import Stock
from app.models import User
from app import db
from services.alpha_vantage import AlphaVantageService

class PortfolioService:
    def __init__(self):
        self.alpha_vantage = AlphaVantageService()
    
    def get_user_portfolio_summary(self, user_id: int):
        user = User.query.get(user_id)
        positions = Stock.query.filter_by(user_id=user_id).all()
        
        portfolio_value = 0
        stocks_data = []
        
        for position in positions:
            quote = self.alpha_vantage.get_stock_quote(position.symbol)
            current_price = float(quote['Global Quote']['05. price'])
            current_value = current_price * position.shares
            portfolio_value += current_value
            
            stocks_data.append({
                'symbol': position.symbol,
                'shares': position.shares,
                'purchase_price': position.purchase_price,
                'current_price': current_price,
                'current_value': current_value
            })
        
        return {
            'cash_balance': user.balance,
            'portfolio_value': portfolio_value,
            'total_value': user.balance + portfolio_value,
            'stocks': stocks_data
        }
    
    def execute_trade(self, user_id: int, symbol: str, action: str, amount: float = None, shares: float = None):
        user = User.query.get(user_id)
        quote = self.alpha_vantage.get_stock_quote(symbol)
        current_price = float(quote['Global Quote']['05. price'])
        
        if amount:
            shares = amount / current_price
            
        if action == 'buy':
            cost = shares * current_price
            if cost > user.balance:
                raise ValueError("Insufficient funds")
                
            user.balance -= cost
            position = Stock.query.filter_by(user_id=user_id, symbol=symbol).first()
            
            if position:
                position.shares += shares
            else:
                position = Stock(
                    user_id=user_id,
                    symbol=symbol,
                    shares=shares,
                    purchase_price=current_price
                )
                db.session.add(position)
                
        elif action == 'sell':
            position = Stock.query.filter_by(user_id=user_id, symbol=symbol).first()
            if not position or position.shares < shares:
                raise ValueError("Insufficient shares")
                
            proceeds = shares * current_price
            user.balance += proceeds
            position.shares -= shares
            
            if position.shares == 0:
                db.session.delete(position)
        
        db.session.commit()
        return self.get_user_portfolio_summary(user_id)
