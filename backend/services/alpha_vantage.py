from flask import current_app
import requests
import os

class AlphaVantageService:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY') # Temporarily use os.getenv() instead of current_app
        self.base_url = 'https://www.alphavantage.co/query'

    def get_stock_quote(self, symbol):
        """
        Get the stock quote (data) for the given symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            dict: The stock quote data from API.
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()


    def get_time_series_daily(self, symbol):
        """
        Get daily time series data for the given symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            dict: The daily time series data.
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()


    def get_time_series_intraday(self, symbol, interval):
        """
        Get per hour time series data for the given symbol.

        Args:
            symbol (str): The stock symbol.
            interval (str): The interval for intraday data.

        Returns:
            dict: The intraday time series data.
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()


    def get_time_series_monthly(self, symbol):
        """
        Get monthly time series data for the given symbol.

        Args:
            symbol (str): The stock symbol.

        Returns:
            dict: The monthly time series data.
        """
        params = {
            'function': 'TIME_SERIES_MONTHLY',
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()


    def get_global_market_status(self):
        """
        Get the global market status of major trading venues.

        Returns:
            dict: The market status data.
        """
        params = {
            'function': 'MARKET_STATUS',
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()
