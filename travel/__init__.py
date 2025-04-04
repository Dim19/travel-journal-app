from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Create a database object that other parts of your app can use.
db = SQLAlchemy()

def create_app():
    # Create a new Flask application instance.
    app = Flask(__name__, static_folder="../static")

    # Set configuration variables.
    app.config["SECRET_KEY"] = "your-secret-key"  # Change this in production!
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.dirname(basedir), "data", "travel.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database with the app.
    db.init_app(app)

    # Import and register the blueprint for routes.
    from travel.routes import travel_bp
    app.register_blueprint(travel_bp)

    return app