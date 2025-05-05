import os

from flask import Flask
# from flask_wtf.csrf import CSRFProtect

from . import db
from . import root


def create_app():
    '''Creates and configures the Flask application.'''

    # Create the base Flask application.
    app = Flask(__name__, instance_relative_config=True)

    # Build path to SQLite3 database.
    db_path = os.path.join(app.instance_path, "webapp.sqlite")

    # Configure the Flask app with a random secret key and database path.
    app.config.from_mapping(SECRET_KEY=os.urandom(16), DATABASE=db_path)

    # Import configuration data from a config file.
    app.config.from_envvar('FLASK_CONFIG_FILE')

    # Create the instance folder if it does not yet exist.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the CSRF protection.
    # csrf = CSRFProtect()
    # csrf.init_app(app)

    # Initialize the database.
    db.init_app(app, db_path)

    # Register the URIs.
    app.register_blueprint(root.bp)

    # Add the root entry point.
    app.add_url_rule("/", endpoint="root")
    return app
