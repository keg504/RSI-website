from email.message import Message
import sys
import logging
from logging import Formatter
from click import confirmation_option
import git
import os

from flask import Flask, redirect, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators
from flask_mail import Mail, Message

STATIC_DIR = os.path.abspath('./static')

# Configure application name
app = Flask(__name__, template_folder='./templates', static_url_path='/static')

# Configure webhook to push website to PythonAnywhere
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./RSI-website')
        origin = repo.remotes.origin
        repo.create_head('main', 
    origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
        origin.pull()
        return '', 200
    else:
        return '', 400

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

@app.route("/research/laptop_cystoscope")
def laptop_cystoscope():
    return render_template("laptop_cystoscope.html")

@app.route("/research/GILLS")
def GILLS():
    return render_template("GILLS.html")

@app.route("/research/renal_stones_URS")
def Renal_stones_URS():
    return render_template("renal_stones_URS.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/affiliates")
def affiliates():
    return render_template("affiliates.html")

@app.route("/leadership")
def leadership():
    return render_template("leadership.html")

@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    class ContactForm(FlaskForm):
        name = StringField("Name")
        email = StringField("Email", [validators.email()])
        subject = StringField("Subject", [validators.Length(min=5)])
        message = TextAreaField("Message", [validators.Length(min=10)])
        send_message = SubmitField()
    form = ContactForm()
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
        return render_template("contact_us.html", form=form)

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