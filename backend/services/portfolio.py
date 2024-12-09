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
        return current_price * stock.quanity
