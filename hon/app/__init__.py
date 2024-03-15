from flask import Flask

from flask_cors import CORS
from .routes import configure_routes

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.secret_key = '1' 
   

    configure_routes(app)

    return app
