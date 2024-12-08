# routes/portfolio.py
from flask import Blueprint, jsonify, request
from models.user import User
from models.stock import Stock
from services.portfolio import PortfolioService  # importing the PortfolioService

portfolio_blueprint = Blueprint('portfolio', __name__)
portfolio_service = PortfolioService()

@portfolio_blueprint.route('/portfolio', methods=['GET'])
def get_portfolio():
    """Fetch a user's portfolio by username."""
    username = request.args.get('username')

    # fetch user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404

    # fetch the user's stocks (portfolio)
    stocks = Stock.query.filter_by(user_id=user.id).all()
    if not stocks:
        return jsonify({'message': 'No stocks in portfolio!'}), 404

    # prepare portfolio data and calculate holding values
    portfolio = []
    total_value = 0
    for stock in stocks:
        holding_value = portfolio_service.calculate_holding_value(stock)
        portfolio.append({
            'symbol': stock.symbol,
            'shares': stock.shares,
            'purchase_price': stock.purchase_price,
            'purchase_date': stock.purchase_date.isoformat(),
            'current_value': holding_value
        })
        total_value += holding_value

    return jsonify({
        'username': user.username,
        'portfolio': portfolio,
        'total_value': total_value
    }), 200
