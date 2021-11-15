import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


load_dotenv()

#TODO add config file .py 

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = "DEV",
        SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{os.environ['PSQL_USER']}:{os.environ['PSWD']}@{os.environ['HOST']}:{os.environ['PORT']}/{os.environ['DB']}",
        DOWNLOAD_FOLDER = f"{os.path.join(os.getcwd(), 'Downloads')}"
    )
    db.init_app(app)
    migrate.init_app(app, db)
    

    from .views import view
    from .api import api
    app.register_blueprint(view, prefix="/")
    app.register_blueprint(api, prefix="/api")
    # app.register_blueprint(api_bp, prefix="/")
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)
    return app
