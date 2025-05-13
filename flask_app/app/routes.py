from flask import Blueprint, render_template

# Create a Blueprint named 'main' for all root-level routes
main = Blueprint('main', __name__)

@main.route("/")
def index():
    """
    Home route for the Flask app.
    Renders the placeholder index page.
    """
    return render_template("index.html")