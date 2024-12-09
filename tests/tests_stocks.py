import pytest
from flask import Flask, jsonify
from unittest.mock import MagicMock
from backend.routes.stocks import bp, AlphaVantageService, PortfolioService
from backend.app import create_app, db
from backend.app.models import User, Portfolio


mock = MagicMock(AlphaVantageService)

# flask app instance for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

# setting up test client
@pytest.fixture
def client(app):
    return app.test_client()

# mock the alpha vantages ervice
@pytest.fixture
def mock_alpha_vantage():

    mock.get_stock_quote.return_value = {
        "Global Quote":
            {
                "01. symbol": "AAPL",
                "02. open": "234.4300",
                "03. high": "238.3800",
                "04. low": "234.2200",
                "05. price": "238.0400",
                "06. volume": "4028430",
                "07. latest trading day": "2024-12-06",
                "08. previous close": "234.7500",
                "09. change": "3.2900",
                "10. change percent": "1.4015%"
            }
    }

    mock.get_time_series_daily.return_value = {
        "Time Series (Daily)": {
            "2024-12-06": {"4. close": "150.00"},
            "2024-12-05": {"4. close": "148.00"},
            "2024-12-04": {"4. close": "145.00"},
            "2024-12-03": {"4. close": "140.00"},
            "2024-12-02": {"4. close": "135.00"},
            "2024-12-01": {"4. close": "130.00"},
            "2024-11-30": {"4. close": "125.00"},
            "2024-11-29": {"4. close": "122.00"},
            "2024-11-28": {"4. close": "118.00"},
            "2024-11-27": {"4. close": "115.00"},
        }
    }

    mock.get_time_series_intraday.return_value = {
        "Time Series (1min)": {
            "2024-12-06 09:30:00": {"1. open": "150.00", "4. close": "150.50"},
            "2024-12-06 09:31:00": {"1. open": "150.50", "4. close": "151.00"},
            "2024-12-06 09:32:00": {"1. open": "151.00", "4. close": "151.50"},
            "2024-12-06 09:33:00": {"1. open": "151.50", "4. close": "152.00"},
            "2024-12-06 09:34:00": {"1. open": "152.00", "4. close": "152.50"},
            "2024-12-06 09:35:00": {"1. open": "152.50", "4. close": "153.00"},
            "2024-12-06 09:36:00": {"1. open": "153.00", "4. close": "153.50"},
            "2024-12-06 09:37:00": {"1. open": "153.50", "4. close": "154.00"},
            "2024-12-06 09:38:00": {"1. open": "154.00", "4. close": "154.50"},
            "2024-12-06 09:39:00": {"1. open": "154.50", "4. close": "155.00"},
        }
    }

    mock.get_time_series_monthly.return_value = {
        "Monthly Time Series": {
            "2024-12-01": {"4. close": "150.00"},
            "2024-11-01": {"4. close": "145.00"},
            "2024-10-01": {"4. close": "140.00"},
            "2024-09-01": {"4. close": "135.00"},
            "2024-08-01": {"4. close": "130.00"},
            "2024-07-01": {"4. close": "125.00"},
            "2024-06-01": {"4. close": "120.00"},
            "2024-05-01": {"4. close": "115.00"},
            "2024-04-01": {"4. close": "110.00"},
            "2024-03-01": {"4. close": "105.00"},
        }
    }

    mock.get_market_status.return_value = {
        "endpoint": "Global Market Open & Close Status",
        "markets": [
            {
                "market_type": "Equity",
                "region": "United States",
                "primary_exchanges": "NASDAQ, NYSE, AMEX, BATS",
                "local_open": "09:30",
                "local_close": "16:15",
                "current_status": "open",
                "notes": ""
            }
        ]
    }

    return mock


# mock the portfolio service
@pytest.fixture
def mock_portfolio():
    mock = MagicMock(PortfolioService)
    return mock

# test of dummy user for buying
@pytest.fixture(scope="module")
def setup_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create dummy user
        dummy_user = User(
            id=1,
            username="dummy",
            email="dummy@test.com",
            password="password",
            balance=1000000.0
        )
        db.session.add(dummy_user)
        db.session.commit()


# test for /api/stock/quote/<symbol>
def test_get_quote(client, mock_alpha_vantage):
    # Mock the service for the test
    symbol = "AAPL"
    response = client.get(f'/api/stock/quote/{symbol}')

    # verify the mock was called and response
    mock_alpha_vantage.get_stock_quote.assert_called_once_with(symbol)
    assert response.status_code == 200
    assert b"150.00" in response.data

    # test with invalid symbol
    mock_alpha_vantage.get_stock_quote.return_value = {"Global Quote": None}
    response = client.get(f'/api/stock/quote/{symbol}')
    assert response.status_code == 500
    assert b"error" in response.data


# test for /api/stock/value/<symbol>/<int:shares>
def test_calculate_value(client, mock_alpha_vantage):
    symbol = "AAPL"
    shares = 10
    response = client.get(f'/api/stock/value/{symbol}/{shares}')

    # verify the value calculation (150.00 * 10 = 1500.00)
    assert response.status_code == 200
    assert b'"value": 1500.0' in response.data

    # test with invalid symbol
    mock_alpha_vantage.get_stock_quote.return_value = {"Global Quote": None}
    response = client.get(f'/api/stock/value/{symbol}/{shares}')
    assert response.status_code == 500
    assert b"error" in response.data


# test for /lookup-stock
def test_lookup_stock(client, mock_alpha_vantage):
    # test with valid symbol
    symbol = "AAPL"
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 200
    assert b"current_price" in response.data
    assert b"AAPL" in response.data

    # test with no symbol
    response = client.get('/lookup-stock?symbol=')
    assert response.status_code == 400
    assert b"No symbol given.." in response.data

    # test with invalid symbol (no data returned)
    mock_alpha_vantage.get_stock_quote.return_value = {"Global Quote": None}
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 404
    assert b"No data found for the given symbol" in response.data

    # test with no market status for valid symbol
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 200
    assert b"market_status" in response.data
    assert b"[]" in response.data


# test for /historical-data
def test_historical_data(client, mock_alpha_vantage):
    # test with valid symbol and range
    symbol = "AAPL"
    response = client.get(f'/historical-data?symbol={symbol}&range=1m')
    assert response.status_code == 200
    assert b"date" in response.data
    assert b"close" in response.data

    # test with no symbol
    response = client.get('/historical-data')
    assert response.status_code == 400
    assert b"Stock name required" in response.data

    # test with invalid symbol
    response = client.get('/lookup-stock?symbol=AAPLT')
    assert response.status_code == 404
    assert b"No historical data found for given symbol" in response.data

    # test with invalid range
    response = client.get(f'/historical-data?symbol={symbol}&range=invalid')
    assert response.status_code == 500
    assert b"Invalid data retrieved!" in response.data



# test for /buy-stock
def test_buy_stock(client, setup_database):
        # test successful buy with sufficient funds
        data = {"symbol": "AAPL", "quantity": 10}
        response = client.post('/api/buy-stock', json=data)
        assert b'"success": true' in response.data
        assert b'"new_balance": 997,619.6' in response.data
        assert b'"portfolio_value": 2,380.4' in response.data


        # test insufficient funds
        data = {"symbol": "AAPL", "quantity": 10000000}
        response = client.post('/api/buy-stock', json=data)
        assert b'"success": false' in response.data
        assert b'"error": "Insufficient funds"' in response.data


        # test invalid stock symbol
        data = {"symbol": "ABCDEKEHOREHO", "quantity": 10}
        response = client.post('/api/buy-stock', json=data)
        assert response.status_code == 400
        assert b'"success": false' in response.data
        assert b'"error": "Invalid stock symbol or API error"' in response.data


        # test ap rate limit reached
        mock.get_stock_quote.return_value = {'Information': "API Rate limit reached"}
        data = {"symbol": "AAPL", "quantity": 10}
        response = client.post('/api/buy-stock', json=data)
        assert response.status_code == 400
        assert b'"success": false' in response.data
        assert b'"error": "API rate limit reached. Please try again later."' in response.data


        # test for invalid quantity (0)
        response = client.post('/api/buy-stock', json={"symbol": "AAPL", "quantity": 0})
        assert response.status_code == 400
        assert b"Invalid quantity" in response.data     # add this case


        # test for invalid quantity (negative)
        response = client.post('/api/buy-stock', json={"symbol": "AAPL", "quantity": -2})
        assert response.status_code == 400
        assert b"Invalid quantity" in response.data     # add this case


        # test for missing JSON fields (symbol)
        response = client.post('/api/buy-stock', json={"quantity": 10})
        assert response.status_code == 400
        assert b"Missing required fields" in response.data     # add this case

        # test for missing JSON fields (quantity)
        response = client.post('/api/buy-stock', json={"symbol": "AAPL"})
        assert response.status_code == 400
        assert b"Missing required fields" in response.data         # add this case


        # test successful buying more stock
        data = {"symbol": "AAPL", "quantity": 10}
        response = client.post('/api/buy-stock', json=data)  #pv = 2,380.4, balance = 997,619.6
        assert b'"success": true' in response.data
        assert b'"new_balance": 997,619.6' in response.data
        assert b'"portfolio_value": 2,380.4' in response.data

        data = {"symbol": "AAPL", "quantity": 10}            #pv = 4,760.8, balance = 995,239.06
        response = client.post('/api/buy-stock', json=data)
        assert b'"success": true' in response.data
        assert b'"new_balance": 995,239.06' in response.data
        assert b'"portfolio_value": 4,760.8' in response.data


        # test failing buying more stock
        data = {"symbol": "AAPL", "quantity": 1000}
        response = client.post('/api/buy-stock', json=data)  #pv = 238,040, balance = 761,960
        assert b'"success": true' in response.data
        assert b'"new_balance": 761,960' in response.data
        assert b'"portfolio_value": 238,040' in response.data

        data = {"symbol": "AAPL", "quantity": 100000}
        response = client.post('/api/buy-stock', json=data)
        assert b'"success": false' in response.data
        assert b'"error": "Insufficient funds"' in response.data


# test for /sell-stock
def test_sell_stock(client):
    # dummy user
    dummy_user = User(username="testuser", balance=100000)
    db.session.add(dummy_user)
    db.session.commit()

    # adding shares
    dummy_portfolio = Portfolio(
        user_id=dummy_user.id,
        symbol = "AAPL",
        quantity = 100,
        purchase_price = 150.00
    )
    db.session.add(dummy_portfolio)
    db.session.commit()

    # test successful selling
    data = {"symbol": "AAPL", "quantity": 10}
    response = client.post('/api/sell-stock', json=data)
    assert b'"success": true' in response.data
    assert b'"new_balance":' in response.data
    assert b'"portfolio_value":' in response.data

    # test selling all the shares
    data = {"symbol": "AAPL", "quantity": 100}
    response = client.post('/api/sell-stock', json=data)
    assert b'"success": true' in response.data
    assert b'"new_balance": 0' in response.data
    assert b'"portfolio_value": 0' in response.data

    # test not enough shares
    data = {"symbol": "AAPL", "quantity": 23000}
    response = client.post('/api/sell-stock', json=data)
    assert b'"success": false' in response.data
    assert b'"error": "Insufficient shares"' in response.data

    # test selling shares of not owned stok
    data = {"symbol": "ROK", "quantity": 10}
    response = client.post('/api/sell-stock', json=data)
    assert b'"success": false' in response.data
    assert b'"error": "Insufficient shares"' in response.data

    # test invalid stock symbol
    data = {"symbol": "%^GBJ()", "quantity": 10}
    response = client.post('/api/sell-stock', json=data)
    assert b'"success": false' in response.data
    assert b'"error": "Invalid stock symbol or API error"' in response.data    # add this error check

    # test api rate limit reached
    mock_alpha_vantage.get_stock_quote.return_value = {"Information": "API Rate limit reached"}
    data = {"symbol": "AAPL", "quantity": 10}
    response = client.post('/api/sell-stock', json=data)
    assert response.status_code == 429
    assert b'"success": false' in response.data
    assert b'"error": "API rate limit reached"' in response.data

    # Test invalid quantity (0)
    response = client.post('/api/sell-stock', json={"symbol": "AAPL", "quantity": 0})
    assert b"No shares sold" in response.data        # add this case

    # Test invalid quantity (negative)
    response = client.post('/api/sell-stock', json={"symbol": "AAPL", "quantity": -10})
    assert response.status_code == 400
    assert b"Invalid quantity" in response.data       # add this case

    # Test missing JSON fields (symbol)
    response = client.post('/api/sell-stock', json={"quantity": 10})
    assert response.status_code == 400
    assert b"Missing required fields" in response.data        # add this case

    # Test missing JSON fields (quantity)
    response = client.post('/api/sell-stock', json={"symbol": "AAPL"})
    assert response.status_code == 400
    assert b"Missing required fields" in response.data          # add this case
