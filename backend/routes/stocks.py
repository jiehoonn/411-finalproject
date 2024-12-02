from flask import Blueprint, jsonify
from services.alpha_vantage import AlphaVantageService
from services.portfolio import PortfolioService

bp = Blueprint('stocks', __name__)
alpha_vantage = AlphaVantageService()
portfolio_service = PortfolioService()

@bp.route('/api/stock/quote/<symbol>')
def get_quote(symbol):
    """Get current stock quote"""
    quote = alpha_vantage.get_stock_quote(symbol)
    return jsonify(quote)

@bp.route('/api/stock/value/<symbol>/<int:shares>')
def calculate_value(symbol, shares):
    """Calculate value of a stock position"""
    quote = alpha_vantage.get_stock_quote(symbol)
    price = float(quote['Global Quote']['05. price'])
    value = price * shares
    return jsonify({'value': value})
