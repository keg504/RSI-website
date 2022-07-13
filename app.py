from email.message import Message
import sys
import logging
from logging import Formatter
from click import confirmation_option

from flask import Flask, redirect, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, validators
from flask_mail import Mail, Message

# Configure application name
app = Flask(__name__)

# App configuration for (this file will not be uploaded to Github)
app.config.from_pyfile('config.py')

# Email initialisation
mail = Mail(app)

# Set up error handler logging
def log_to_stderr(app):
  handler = logging.StreamHandler(sys.stderr)
  handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
  ))
  handler.setLevel(logging.WARNING)
  app.logger.addHandler(handler)

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

# Test route for forms, remove/change in production
@app.route("/test_form", methods=["GET", "POST"])
def test_form():
    class TestForm(FlaskForm):
        name = StringField("Name")
        email = StringField("Email", [validators.email()])
        subject = StringField("Subject", [validators.Length(min=5)])
        message = TextAreaField("Message", [validators.Length(min=10)])
        recaptcha = RecaptchaField()
        send_message = SubmitField()
    form = TestForm()
    if form.validate_on_submit():
        contact_msg = {
            "name" : form.name.data,
            "email" : form.email.data,
            "subject" : form.subject.data,
            "message" : form.message.data
        }

        msg = Message(contact_msg["subject"], sender=(f"RSI website: {contact_msg['name']}", contact_msg['email']))
        msg.body = f"From: {contact_msg['name']} ({contact_msg['email']})\nSubject: {contact_msg['subject']}\n\n{contact_msg['message']}"
        msg.recipients = ["test@mailtrap.io"]
        print(msg)
        mail.send(msg)
        return redirect("/send_confirmation")
    else:
        return render_template("test_form.html", form=form)

@app.route("/send_confirmation")
def send_confirmation():
    return render_template("send_confirmation.html")

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
    log_to_stderr(app)
    # Set debug mode to True for development
    app.run(host="localhost")