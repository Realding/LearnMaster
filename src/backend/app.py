from flask import Flask
from flask_migrate import Migrate
from .models.db import db
from .setting import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        from .views import views
    print(app.config['JSON_AS_ASCII'])
    return app
