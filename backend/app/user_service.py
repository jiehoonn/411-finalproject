from backend.app.models import db, User

def create_user(username, email, password):
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists")

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user
