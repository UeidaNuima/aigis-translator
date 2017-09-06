from flask import Flask
from .api_1_0 import api as api_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint, url_prefix='/1.0')
    return app
