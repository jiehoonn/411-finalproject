from typing import List, Dict
from models.stock import Stock
from services.alpha_vantage import AlphaVantageService

class PortfolioService:
    def __init__(self):
        self.alpha_vantage = AlphaVantageService()

    def calculate_holding_value(self, stock):
        quote = self.alpha_vantage.get_stock_quote(stock.symbol)
        
        if 'Information' in quote:
            # Return last known price if API limit reached
            return stock.purchase_price * stock.quantity
            
        if 'Global Quote' not in quote:
            return stock.purchase_price * stock.quantity
            
        current_price = float(quote['Global Quote']['05. price'])
        return current_price * stock.quantity

