from flask_migrate import Migrate

migrate = Migrate()
migrate.init_app(app, db)
