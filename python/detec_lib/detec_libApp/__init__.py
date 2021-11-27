import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

python_folder, _ = os.path.split(os.getcwd())
template_folder_path = os.path.join(python_folder, "templates")
static_folder_path = os.path.join(python_folder, "static", __name__)
template_prefix = __name__

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'DEV',
        SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{os.environ['PSQL_USER']}:{os.environ['PSWD']}@{os.environ['HOST']}:{os.environ['PORT']}/{os.environ['DB_lib']}",
    )
    app.template_folder = template_folder_path
    app._static_folder = static_folder_path
    db.init_app(app)
    migrate.init_app(app, db)

    from .param_views import params
    from .foil_views import foils
    app.register_blueprint(params, prefix="/")
    app.register_blueprint(foils, prefix="/")

    return app


