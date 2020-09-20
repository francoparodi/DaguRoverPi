from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    from flaskr.models import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)

    from flaskr.routes import view
    app.register_blueprint(view)

    return app
