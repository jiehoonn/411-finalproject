import pytest
from flask import Flask, jsonify
from unittest.mock import MagicMock
from stocks import bp, AlphaVantageService, PortfolioService

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
    mock = MagicMock(AlphaVantageService)
    mock.get_stock_quote.return_value = {
        "Global Quote": {"05. price": "150.00"}
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
            "2024-11-26": {"4. close": "112.00"},
            "2024-11-25": {"4. close": "110.00"},
            "2024-11-24": {"4. close": "107.00"},
            "2024-11-23": {"4. close": "105.00"},
            "2024-11-22": {"4. close": "103.00"},
            "2024-11-21": {"4. close": "102.00"},
            "2024-11-20": {"4. close": "101.00"},
            "2024-11-19": {"4. close": "100.00"},
            "2024-11-18": {"4. close": "99.00"},
            "2024-11-17": {"4. close": "98.00"},
            "2024-11-16": {"4. close": "97.00"},
            "2024-11-15": {"4. close": "96.00"},
            "2024-11-14": {"4. close": "95.00"},
            "2024-11-13": {"4. close": "94.00"},
            "2024-11-12": {"4. close": "93.00"},
            "2024-11-11": {"4. close": "92.00"},
            "2024-11-10": {"4. close": "91.00"},
            "2024-11-09": {"4. close": "90.00"},
            "2024-11-08": {"4. close": "89.00"},
            "2024-11-07": {"4. close": "88.00"},
            "2024-11-06": {"4. close": "87.00"},
            "2024-11-05": {"4. close": "86.00"},
            "2024-11-04": {"4. close": "85.00"},
            "2024-11-03": {"4. close": "84.00"},
            "2024-11-02": {"4. close": "83.00"},
            "2024-11-01": {"4. close": "82.00"},
            "2024-10-31": {"4. close": "81.00"},
            "2024-10-30": {"4. close": "80.00"},
            "2024-10-29": {"4. close": "79.00"},
            "2024-10-28": {"4. close": "78.00"},
            "2024-10-27": {"4. close": "77.00"},
            "2024-10-26": {"4. close": "76.00"},
            "2024-10-25": {"4. close": "75.00"},
            "2024-10-24": {"4. close": "74.00"},
            "2024-10-23": {"4. close": "73.00"},
            "2024-10-22": {"4. close": "72.00"},
            "2024-10-21": {"4. close": "71.00"},
            "2024-10-20": {"4. close": "70.00"},
            "2024-10-19": {"4. close": "69.00"},
            "2024-10-18": {"4. close": "68.00"},
            "2024-10-17": {"4. close": "67.00"},
            "2024-10-16": {"4. close": "66.00"},
            "2024-10-15": {"4. close": "65.00"},
            "2024-10-14": {"4. close": "64.00"},
            "2024-10-13": {"4. close": "63.00"},
            "2024-10-12": {"4. close": "62.00"},
            "2024-10-11": {"4. close": "61.00"},
            "2024-10-10": {"4. close": "60.00"},
            "2024-10-09": {"4. close": "59.00"},
            "2024-10-08": {"4. close": "58.00"},
            "2024-10-07": {"4. close": "57.00"},
            "2024-10-06": {"4. close": "56.00"},
            "2024-10-05": {"4. close": "55.00"}
        }
    }
    return mock

# mock the portfolio service
@pytest.fixture
def mock_portfolio():
    mock = MagicMock(PortfolioService)
    return mock

# test for /api/stock/quote/<symbol>
def test_get_quote(client, mock_alpha_vantage):
    # Mock the service for the test
    symbol = "AAPL"
    response = client.get(f'/api/stock/quote/{symbol}')
    
    # verify the mock was called and response
    mock_alpha_vantage.get_stock_quote.assert_called_once_with(symbol)
    assert response.status_code == 200
    assert b"150.00" in response.data

# test for /api/stock/value/<symbol>/<int:shares>
def test_calculate_value(client, mock_alpha_vantage):
    symbol = "AAPL"
    shares = 10
    response = client.get(f'/api/stock/value/{symbol}/{shares}')
    
    # verify the value calculation (150.00 * 10 = 1500.00)
    assert response.status_code == 200
    assert b'"value": 1500.0' in response.data

# test for /lookup-stock
def test_lookup_stock(client, mock_alpha_vantage):
    # test with valid symbol
    symbol = "AAPL"
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 200
    assert b"current_price" in response.data
    assert b"AAPL" in response.data
    
    # test with no symbol
    response = client.get('/lookup-stock')
    assert response.status_code == 400
    assert b"error" in response.data
    
    # test with invalid symbol (no data returned)
    mock_alpha_vantage.get_stock_quote.return_value = {"Global Quote": None}
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 404
    assert b"error" in response.data

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
    assert b"error" in response.data

    # test with invalid range
    response = client.get(f'/historical-data?symbol={symbol}&range=invalid')
    assert response.status_code == 500
    assert b"Invalid data retrieved!" in response.data
