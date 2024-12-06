from backend.app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Float, default=1000000.00)  # Starting balance
    stocks = db.relationship('Stock', backref='owner', lazy=True)

    def set_password(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    def get_portfolio_value(self):
        return sum(stock.get_current_value() for stock in self.stocks)
