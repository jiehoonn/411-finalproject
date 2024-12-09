from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # Drop all tables to start fresh
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
