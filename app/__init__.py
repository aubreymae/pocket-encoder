import os
from flask import Flask
from flask_cors import CORS, cross_origin

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", 
        DATABASE=os.path.join(app.instance_path, "upload-db.db"),
        UPLOAD_FOLDER=os.path.join(app.root_path, "uploads"),
        PROCESSED_FOLDER=os.path.join(app.root_path, "processed")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["PROCESSED_FOLDER"], exist_ok=True)

    from . import db
    db.init_app(app)

    from app.routes import api
    app.register_blueprint(api)

    return app