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
from controllers.order_comic_controller import order_comic_bp
from validators.validators import register_error_handlers


"""
Flask Application: configures DB, error handlers and blueprints.
"""

# Create and configure the app instance
def create_app():
    app = Flask(__name__)

    # Set the SQLAlchemy connection
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    
    # Initialize extensions
    db.init_app(app)

    # keeps Json order as defined in schemas
    app.json.sort_keys = False

    # CLI Blueprint
    app.register_blueprint(database_controller)

    # API Blueprints
    app.register_blueprint(costumer_bp) 
    app.register_blueprint(artist_bp)
    app.register_blueprint(writer_bp)
    app.register_blueprint(publisher_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(comic_bp)
    app.register_blueprint(order_comic_bp)

    # Centralized Error Handler
    register_error_handlers(app)
    return app