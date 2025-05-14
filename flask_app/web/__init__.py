from flask import Flask
import os  # Add this to build the correct template path


def create_app():
    # Resolve absolute path to the templates directory
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "templates")
    )
    print("TEMPLATE PATH:", template_dir)  # Debug output for confirmation

    # Explicitly tell Flask where to find templates
    app = Flask(__name__, template_folder=template_dir)

    # Import and register route blueprints
    from .routes import main

    app.register_blueprint(main)

    return app
