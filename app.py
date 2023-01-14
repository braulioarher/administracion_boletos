import os

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from db import db
import models

from resources.event import blp as EventBlueprint
from resources.ticket import blp as TicketBlueprint

def create_app(db_url=None):

    app = Flask(__name__)

    # Variables de entorno de nuestra app
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Events API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    migrate = Migrate(app, db)

    # Creacion de api
    api = Api(app)

    api.register_blueprint(EventBlueprint)
    api.register_blueprint(TicketBlueprint)

    return app