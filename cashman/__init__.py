from flask import Flask
from .models import db
from .views import bp  # your blueprint
from flask_marshmallow import Marshmallow

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cashman.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(bp)  # register your routes

    with app.app_context():
        db.create_all()  # creates tables

    return app
