import sqlite3

from datetime import datetime
from flask import current_app
from flask import g


def get_db():
    '''Returns a handle to the SQLite3 database.'''

    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):  # pylint: disable=unused-argument
    '''Closes the handle to the database and de-registers it from the global object.'''

    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app, db_path):
    '''Initializes the database system.'''

    # Ensure that the database is closed upon application termination.
    app.teardown_appcontext(close_db)

    # Ensure that the database table exists.
    with sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES) as _db:
        _db.executescript("""CREATE TABLE IF NOT EXISTS form_data(user_input TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);""")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))
