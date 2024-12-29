#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://127.0.0.1:5000"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

# Function to check the health of the service
check_health() {
    echo "Checking health status..."
    response=$(curl -s -X GET "$BASE_URL/health")
    if [ "$ECHO_JSON" = true ]; then
        echo "Response: $response"
    fi
    # Remove whitespace before comparing
    if echo "$response" | tr -d '[:space:]' | grep -q '"status":"healthy"'; then
        echo "Service is healthy."
    else
        echo "Health check failed."
        echo "Full response was: $response"
        exit 1
    fi
}

# Function to test user registration
test_registration() {
  echo "Testing user registration..."
  response=$(curl -s -X POST "$BASE_URL/api/auth/register" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "email":"test@example.com", "password":"password123"}')
  if [ "$ECHO_JSON" = true ]; then
    echo "Registration Response:"
    echo "$response"
  fi
}

# Function to test user login
test_login() {
  echo "Testing user login..."
  response=$(curl -s -X POST "$BASE_URL/api/auth/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if [ "$ECHO_JSON" = true ]; then
    echo "Login Response:"
    echo "$response"
  fi
}

# Function to test stock quote
test_stock_quote() {
  echo "Testing stock quote..."
  response=$(curl -s -X GET "$BASE_URL/api/stock/quote/AAPL")
  if [ "$ECHO_JSON" = true ]; then
    echo "Stock Quote Response:"
    echo "$response"
  fi
}

# Function to test password update
test_update_password() {
    echo "Testing password update..."
    response=$(curl -s -X PUT "$BASE_URL/api/auth/update-password" -H "Content-Type: application/json" \
        -d '{"username":"testuser", "current_password":"password123", "new_password":"newpassword456"}')
    if [ "$ECHO_JSON" = true ]; then
        echo "Update Password Response:"
        echo "$response"
    fi
}

# Function to test stock value calculation
test_stock_value() {
    echo "Testing stock value calculation..."
    response=$(curl -s -X GET "$BASE_URL/api/stock/value/AAPL/10")
    if [ "$ECHO_JSON" = true ]; then
        echo "Stock Value Response:"
        echo "$response"
    fi
}

# Function to test stock lookup
test_lookup_stock() {
    echo "Testing stock lookup..."
    response=$(curl -s -X GET "$BASE_URL/lookup-stock?symbol=AAPL")
    if [ "$ECHO_JSON" = true ]; then
        echo "Stock Lookup Response:"
        echo "$response"
    fi
}

# Function to test historical data
test_historical_data() {
    echo "Testing historical data..."
    response=$(curl -s -X GET "$BASE_URL/historical-data?symbol=AAPL&range=1m")
    if [ "$ECHO_JSON" = true ]; then
        echo "Historical Data Response:"
        echo "$response"
    fi
}

# Function to test portfolio status
test_portfolio_status() {
    echo "Testing portfolio status..."
    # Get user ID from login response
    login_response=$(curl -s -X POST "$BASE_URL/api/auth/login" -H "Content-Type: application/json" \
        -d '{"username":"testuser", "password":"password123"}')
    user_id=$(echo $login_response | grep -o '"id":[0-9]*' | cut -d':' -f2)
    
    response=$(curl -s -X GET "$BASE_URL/api/portfolio-status/$user_id")
    if [ "$ECHO_JSON" = true ]; then
        echo "Portfolio Status Response:"
        echo "$response"
    fi
}

# Function to test buy stock
test_buy_stock() {
    echo "Testing buy stock..."
    response=$(curl -s -X POST "$BASE_URL/api/buy-stock" -H "Content-Type: application/json" \
        -d '{"symbol":"AAPL", "quantity":1, "userId":1}')
    if [ "$ECHO_JSON" = true ]; then
        echo "Buy Stock Response:"
        echo "$response"
    fi
}

# Function to test sell stock
test_sell_stock() {
    echo "Testing sell stock..."
    response=$(curl -s -X POST "$BASE_URL/api/sell-stock" -H "Content-Type: application/json" \
        -d '{"symbol":"AAPL", "quantity":1, "userId":1}')
    if [ "$ECHO_JSON" = true ]; then
        echo "Sell Stock Response:"
        echo "$response"
    fi
}

# Update the test execution section at the bottom of the file:
check_health
test_registration
test_login
test_update_password
test_stock_quote
test_stock_value
test_lookup_stock
test_historical_data
test_portfolio_status
test_buy_stock
test_sell_stock

echo "All smoke tests completed!"