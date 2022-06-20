from flask import Flask, render_template
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

if __name__ == "__main__":
    app.run()