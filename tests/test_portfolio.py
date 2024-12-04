import pytest
from services.portfolio import PortfolioService
from models.stock import Stock

def test_calculate_holding_value():
    """Test portfolio value calculation"""
    portfolio_service = PortfolioService()
    stock = Stock(symbol='AAPL', shares=10, purchase_price=150.00)
    value = portfolio_service.calculate_holding_value(stock)
    assert isinstance(value, float)
    assert value > 0
