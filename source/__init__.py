from flask import Flask
from mongoengine import connect


def create_app():
    app = Flask(__name__)
    
    app.config["MONGODB_SETTINGS"] = {
        "db": "cosplay",
        "host": "localhost",
        "port": 27017
    }
    
    connect(**app.config["MONGODB_SETTINGS"])
    
    from source.main.controllers import register_routes
    register_routes(app)
    
    return app