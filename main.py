from flask import Flask
from init import db
from controllers.cli_controllers import database_controller
import os

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    db.init_app(app)
    app.register_blueprint(database_controller)
    return app