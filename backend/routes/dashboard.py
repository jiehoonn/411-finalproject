from flask import Blueprint, jsonify, request
from middleware.auth import login_required
from services.portfolio import PortfolioService
from services.alpha_vantage import AlphaVantageService

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
portfolio_service = PortfolioService()
alpha_vantage = AlphaVantageService()

@bp.route('/balance', methods=['GET'])
@login_required
def get_balance():
    user = request.user
    return jsonify({
        'balance': user.balance,
        'username': user.username
    })

@bp.route('/portfolio-summary', methods=['GET'])
@login_required
def get_portfolio_summary():
    portfolio_data = portfolio_service.get_user_portfolio_summary(request.user.id)
    return jsonify(portfolio_data)

@bp.route('/trade', methods=['POST'])
@login_required
def execute_trade():
    data = request.json
    try:
        result = portfolio_service.execute_trade(
            user_id=request.user.id,
            symbol=data['symbol'],
            action=data['action'],
            amount=data.get('amount'),
            shares=data.get('shares')
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
