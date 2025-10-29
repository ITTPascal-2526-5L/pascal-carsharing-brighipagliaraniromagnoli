from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 

    from .routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app