import sys
import logging
from logging import Formatter

from flask import Flask, render_template
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology
from wtforms import Form, StringField
from flask_mail import Mail

# Set up error handler logging
def log_to_stderr(app):
  handler = logging.StreamHandler(sys.stderr)
  handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
  ))
  handler.setLevel(logging.WARNING)
  app.logger.addHandler(handler)

# Configure application
app = Flask(__name__)

# Website page routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/research")
def research():
    return render_template("research.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/affiliates")
def affiliates():
    return render_template("affiliates.html")

@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    return render_template("contact_us.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# To be build out after static part of website is complete and live
# Requires libraries that have not been installed or imported yet, so leave commented for later

# @app.route("/surgical_records")
# @login_required
# def surgical_records():
#     return render_template("surgical_records.html")

# Error handling function for displaying HTTP errors
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

if __name__ == "__main__":
    app.run()