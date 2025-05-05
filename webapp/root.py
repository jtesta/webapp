import datetime
import jwt

from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import request

from .db import get_db


bp = Blueprint("bp", __name__)


def handle_request(_request, html_page, page_number):
    '''Handles web application GET and POST requests.'''

    # When an HTTP GET request is received, simply return the blank form.
    if _request.method == "GET":
        return render_template(html_page, google_signin_client_id=current_app.config["GOOGLE_SIGNIN_CLIENT_ID"], page_number=page_number)

    # When a POST request is received, insert the user's input into the database and render the output back into the page.
    if _request.method == "POST":
        output_class = "normal"

        # Get a timestamp, convert it to a string for insertion into the database, then also convert it to a human-readable version.
        timestamp = datetime.datetime.now()
        timestamp_db = str(timestamp)
        timestamp_ui = timestamp.strftime("%Y-%m-%d %I:%M:%S%p")

        # Read the textbox data that the user submitted.
        user_input = _request.form["user_input"]

        current_app.logger.debug(f"Submitted to {_request.path}: {user_input}")

        # Since we're building the SQL query directly from user input, this is vulnerable to SQL injection!
        db = get_db()
        db.execute("INSERT INTO form_data VALUES (\"" + user_input + "\", \"" + timestamp_db + "\")")
        db.commit()

        # Determine if a JWT was submitted.
        if page_number == "2":

            # Ensure that there are exactly three fields separated by a period.
            fields = user_input.split(".")
            if len(fields) == 3:

                # Ensure that the payload and signature fields are greater than length zero.
                header = fields[0]
                payload = fields[1]
                signature = fields[2]
                if len(header) > 0 and len(payload) > 0 and len(signature) > 0:

                    # We found a valid JWT structure.
                    public_key = current_app.config["JWT_ES256_PUBLIC_KEY"]

                    try:
                        jwt.decode(user_input, public_key, algorithms=["ES256"])
                        output_class = "valid_jwt"

                        # Log the fact that we received a valid JWT.
                        current_app.logger.info(f"Valid JWT found: {user_input}")
                    except jwt.exceptions.InvalidSignatureError:
                        # Log the fact that we received an invalid JWT.
                        current_app.logger.info(f"Invalid JWT found: {user_input}")

        return render_template(html_page, google_signin_client_id=current_app.config["GOOGLE_SIGNIN_CLIENT_ID"], page_number=page_number, user_input=user_input, timestamp=timestamp_ui, output_class=output_class)

    raise NotImplementedError("Only GET and POSTs are allowed.")


# This will return links to /page1 and /page2.
@bp.route("/", methods=["GET"])
def root():
    '''Returns the root page, which has links to /page1 and /page2.'''

    return render_template("index.html")


@bp.route("/page1", methods=["GET", "POST"])
def page1():
    '''Handles GETs and POSTs to /page1.'''

    return handle_request(request, "page.html", "1")


@bp.route("/page2", methods=["GET", "POST"])
def page2():
    '''Handles GETs and POSTs to /page2'''

    return handle_request(request, "page.html", "2")
