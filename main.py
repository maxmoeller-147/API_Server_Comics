import os

from flask import Flask

from init import db
from controllers.cli_controllers import database_controller
from controllers.costumer_controller import costumer_bp
from controllers.artist_controller import artist_bp
from controllers.writer_controller import writer_bp
from controllers.publisher_controller import publisher_bp
from controllers.order_controller import order_bp
from controllers.comic_controller import comic_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    db.init_app(app)
    app.json.sort_keys = False
    app.register_blueprint(database_controller)
    app.register_blueprint(costumer_bp) 
    app.register_blueprint(artist_bp)
    app.register_blueprint(writer_bp)
    app.register_blueprint(publisher_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(comic_bp)
    return app