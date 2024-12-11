# Stock Trading Application

A stock trading platform that enables individual users to manage portfolios, make trades, and monitor market conditions using the Alpha Vantage API.

## Features

### 1. View Portfolio

- Display digital balance
- Display overall portfolio value
- Integration of the latest stock prices
- **API Endpoints Used**: Quote Endpoint

### 2. Buy Stock

- Purchase shares with specified stock symbol and quantity
- **API Endpoints Used**: Quote Endpoint 

### 3. Sell Stock

- Sell shares from current holdings
- **API Endpoints Used**: Quote Endpoint 

### 4. Look Up Stock

- Detailed stock information
- Current market price and volume
- Global market status
- **API Endpoints Used**: Quote and Global Market Open & Close Status Endpoint

### 5. Stock Trends (Historical Data)

- Stock trends from the past 1 day, 10 days, 1 month, 6 month and 1 year
- **API Endpoints Used**: Time Series Daily, Time Series Intraday and Time Series Monthly Endpoint



## Technical Implementation

### Core Features and Routes

#### User Account Management

- **Routes**: `/create-account`, `/login`, `/update-password`
- Secure password storage with salted hashing
- Input validation
- SQLite database storage

#### Portfolio Management

- **Route**: `/portfolio`
- Live stock data integration
- Dynamic portfolio calculations

#### Trading Operations

- **Routes**: `/buy-stock`, `/sell-stock`
- Real-time price fetching
- Transaction validation
- Virtual wallet management

#### Stock Information

- **Route**: `/lookup-stock`
- Detailed stock data
- Caching implementation
- Historical data visualization

#### Analytics

- **Route**: `/historical-data`
- Visual data representation
- Customizable date ranges
- **API Endpoints Used**: Time Series Daily, Monthly, and Weekly Endpoints

## Running the application

1. **Clone the repository:**

   ```bash
   git clone [your-repository-url]
   ```

2. **Navigate to the project directory:**

   ```bash
   cd [project-name]
   ```

3. **Activate the virtual environment for frontend:**

   ```bash
   cd frontend
   source venv/bin/activate
   ```

3. **Install frontend dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the React Application:**
   ```bash
   npm start
   ```
  

5. **In a seperate terminal, activate the virtual environment for the backend:**

   ```bash
   cd /backend
   source venv/bin/activate
   ```

8. **Install backend dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
   

9.**Run the Flask Application:**
   ```bash
   python3 -m flask run
   ```

10. **Add your API key to the backend env file:**




## API and Database Used

- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- Key endpoints used: Quote, Time Series Daily, Time Series IntraDay, Time Series Monthly and Global Market Open & Close Status 
- Database: SQLAlchemy


## Route Documentation

### 1. Register

- **Route**: `/register  
- **Request Type**: POST  
- **Purpose**: Creates a new user account with a username, email and password.  

**Request Body**:  
- `username` (String): The username of the user.  
- `email` (String): The email address of the user.  
- `password` (String): The password of the user.  

#### Response Format: JSON
**Success Response Example:**
- Code: 200
- Content:
```json
  {
      "message": "User registered successfully",
      "user": {
          "username": "newuser123",
          "email": "newuser123@example.com",
          "balance": 1000000.0
      }
  }
  ```
#### **Example Request**:  
```json
{
    "username": "newuser123",
    "email": "newuser123@example.com",
    "password": "pass123"
}
```  

#### **Example Response**:  
```json
{
    "message": "User registered successfully",
    "user": {
        "username": "newuser123",
        "email": "newuser123@example.com",
        "balance": 1000000.0
    }
}
```
---

### 2. Login

- **Route**: `/login`  
- **Request Type**: POST  
- **Purpose**: Used to authenticate an existing user with their username and password.  

#### **Request Body**:  
- `username` (String): The username of the user.  
- `password` (String): The password of the user.

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "message": "Login successful",
      "user": {
          "id": 1,
          "username": "existinguser",
          "email": "existinguser@example.com",
          "balance": 1000000.0
      }
  }
  ```

##### **Error Responses**:  
1. **Code**: 400  
   **Content**:  
   ```json
   { "error": "Missing required fields" }
   ```  

2. **Code**: 401  
   **Content**:  
   ```json
   { "error": "Invalid credentials" }
   ``` 

#### **Example Request**:  
```json
{
    "username": "existinguser",
    "password": "password123"
}
```  

#### **Example Response**:  
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "existinguser",
        "email": "existinguser@example.com",
        "balance": 1000000.0
    }
}
```

---

### 3. Update Password

- **Route**: `/update-password`  
- **Request Type**: POST  
- **Purpose**: Allows a user to update their password.  

#### **Request Body**:  
- `username` (String): The username of the user.  
- `current_password` (String): The user's current password.  
- `new_password` (String): The new password.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "message": "Password updated successfully"
  }
  ```  

##### **Error Responses**:  
1. **Code**: 400  
   **Content**:  
   ```json
   { "error": "Missing required fields" }
   ```  

2. **Code**: 404  
   **Content**:  
   ```json
   { "error": "User not found" }
   ```  

3. **Code**: 401  
   **Content**:  
   ```json
   { "error": "Current password is incorrect" }
   ```

#### **Example Request**:  
```json
{
    "username": "existinguser",
    "current_password": "oldpassword",
    "new_password": "newsecurepassword"
}
```  

#### **Example Response**:  
```json
{
    "message": "Password updated successfully"
}
```

---

### Get Stock Quote

- **Route**: `/api/stock/quote/<symbol>`
- **Request Type**: GET  
- **Purpose**: Fetches the current stock data for the given stock symbol.

#### **Path Parameters**:  
- `symbol` (String): The stock symbol for which data is to be fetched.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "Global Quote": {
          "01. symbol": "AAPL",
          "05. price": "150.00",
          "06. volume": "1000000"
      }
  }
  ```  

##### **Error Responses**:  
1. **Code**: 500  
   **Content**:  
   ```json
   { "error": "Failed to fetch stock quote" }
   ```

   #### **Example Request**:  
```http
GET host/api/stock/quote/IBM
```

#### **Example Response**:  
```json
{
   "Global Quote": {
   "01. symbol": "IBM",
   "02. open": "228.4000",
   "03. high": "234.3900",
   "04. low": "227.8000",
   "05. price": "231.7200",
   "06. volume": "4769531",
   "07. latest trading day": "2024-12-10",
   "08. previous close": "230.0000",
   "09. change": "1.7200",
   "10. change percent": "0.7478%"
   }
}
```

---

### Calculate Value

- **Route**: `/api/stock/value/<symbol>/<int:shares>`
- **Request Type**: GET  
- **Purpose**: Calculates the total value of a stock position based on the current stock price and the number of shares.

#### **Path Parameters**:  
- `symbol` (String): The stock symbol.  
- `shares` (Integer): The number of shares owned.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "value": 3000.0
  }
  ```  

##### **Error Responses**:  
1. **Code**: 500  
   **Content**:  
   ```json
   { "error": "Failed to calculate stock value" }
   ```
   
#### **Example Request**:  
```http
GET /api/stock/value/AAPL/20 HTTP/1.1
Host: example.com
```

#### **Example Response**:  
```json
{
    "value": 3000.0
}
```
---

### Lookup Stock

- **Route**: `\lookup-stock`
- **Request Type**: GET  
- **Purpose**: Fetches the current stock data and market status for a specified stock symbol.

#### **Query Parameters**:  
- `symbol` (String): The stock symbol to look up.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "symbol": "AAPL",
      "current_price": "150.00",
      "volume": "1000000",
      "market_status": [
          {
              "market_type": "Stock Market",
              "region": "US",
              "current_status": "Open"
          }
      ]
  }
  ```  

##### **Error Responses**:  
1. **Code**: 400  
   **Content**:  
   ```json
   { "error": "No symbol given" }
   ```

2. **Code**: 404  
   **Content**:  
   ```json
   { "error": "No data found for the given symbol" }
   ```

3. **Code**: 500  
   **Content**:  
   ```json
   { "error": "Error getting stock data" }
   ```

#### **Example Request**:  
```http
GET host/lookup-stock?symbol=AAPL
```

#### **Example Response**:  
```json
{
    "symbol": "AAPL",
    "current_price": "150.00",
    "volume": "1000000",
    "market_status": [
        {
            "market_type": "Stock Market",
            "region": "US",
            "current_status": "Open"
        }
    ]
}
```


---

### Historical Data

- **Route**: `\historical-data``
- **Request Type**: GET  
- **Purpose**: Fetches historical trend data for the specified stock symbol within a given time range.

#### **Query Parameters**:  
- `symbol` (String): The stock symbol.  
- `range` (String): The time range (e.g., '1d', '10d', '1m'). Defaults to '1m'.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  [
      { "date": "2023-12-01", "close": 150.0 },
      { "date": "2023-12-02", "close": 152.0 }
  ]
  ```  

##### **Error Responses**:  
1. **Code**: 400  
   **Content**:  
   ```json
   { "error": "No symbol given" }
   ```

2. **Code**: 500  
   **Content**:  
   ```json
   { "error": "Failed to fetch historical trend data" }
   ```

#### **Example Request**:  
```http
GET host/historical-data?symbol=AAPL&range=1m 
```

#### **Example Response**:  
```json
[
    { "date": "2023-12-01", "close": 150.0 },
    { "date": "2023-12-02", "close": 152.0 }
]
```

---

### Portfolio Status

- **Route**: `/api/portfolio-status/<int:user_id>`
- **Request Type**: GET  
- **Purpose**: Fetches the portfolio status for a user, including account balance and portfolio value.

#### **Path Parameters**:  
- `user_id` (Integer): The user ID.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "balance": 1000.0,
      "portfolio_value": 5000.0
  }
  ```  

##### **Error Responses**:  
1. **Code**: 404  
   **Content**:  
   ```json
   { "error": "No user found" }
   ```

#### **Example Request**:  
```http
GET /api/portfolio-status/1 HTTP/1.1
Host: example.com
```

#### **Example Response**:  
```json
{
    "balance": 1000.0,
    "portfolio_value": 5000.0
}
```

---

### Buy Stock

- **Route**: - `/api/buy-stock`
- **Request Type**: POST  
- **Purpose**: Buys stock(s) for a user and updates their portfolio value and account balance.

#### **Request Body**:  
- `symbol` (String): The stock symbol.  
- `quantity` (Integer): The number of shares to buy.  
- `userId` (Integer): The user ID.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "success": true,
      "new_balance": 900.0,
      "portfolio_value": 1500.0
  }
  ```  

##### **Error Responses**:  
1. **Code**: 400  
   **Content**:  
   ```json
   { "success": false, "error": "Invalid input" }
   ```

2. **Code**: 404  
   **Content**:  
   ```json
   { "success": false, "error": "User not found" }
   ```

3. **Code**: 400  
   **Content**:  
   ```json
   { "success": false, "error": "Insufficient funds" }
   ```
#### **Example Request**:  
```http
POST /api/buy-stock HTTP/1.1
Host: example.com
Content-Type: application/json

{
    "symbol": "AAPL",
    "quantity": 10,
    "userId": 1
}
```

#### **Example Response**:  
```json
{
    "success": true,
    "new_balance": 900.0,
    "portfolio_value": 1500.0
}
```

---

### Route Documentation: `/api/sell-stock`

- **Route** : `/api/sell-stock`
- **Request Type**: POST  
- **Purpose**: Sells stock(s) for a user and updates their portfolio value and account balance.

#### **Request Body**:  
- `symbol` (String): The stock symbol.  
- `quantity` (Integer): The number of shares to sell.  
- `userId` (Integer): The user ID.  

#### **Response Format**: JSON  

##### **Success Response Example**:  
- **Code**: 200  
- **Content**:  
  ```json
  {
      "success": true,
      "new_balance": 1100.0,
      "portfolio_value": 500.0
  }
  ```  

##### **Error Responses**:  
1. **Code**: 400  
   **Content**:  
   ```json
   { "success": false, "error": "Invalid input" }
   ```

2. **Code**: 404  
   **Content**:  
   ```json
   { "success": false, "error": "User not found" }
   ```

3. **Code**: 400  
   **Content**:  
   ```json
   { "success": false, "error": "Insufficient shares" }

#### **Example Request**:  
```http
POST /api/sell-stock HTTP/1.1
Host: example.com
Content-Type: application/json

{
    "symbol": "AAPL",
    "quantity": 5,
    "userId": 1
}
```

#### **Example Response**:  
```json
{
    "success": true,
    "new_balance": 1100.0,
    "portfolio_value": 500.0
}
   
