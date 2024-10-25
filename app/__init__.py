from flask import Flask
from flask_cors import CORS
from .routes import segment_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register routes
    app.register_blueprint(segment_blueprint)

    return app
