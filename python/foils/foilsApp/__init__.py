import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

python_folder, _ = os.path.split(os.getcwd())
template_folder_path = os.path.join(python_folder, "templates")
static_folder_path = os.path.join(python_folder, "static", __name__)
template_prefix = __name__

load_dotenv()
#TODO add config file .py 

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = "DEV",
        SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{os.environ['PSQL_USER']}:{os.environ['PSWD']}@{os.environ['HOST']}:{os.environ['PORT']}/foildetectors"
        # SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{os.environ['PSQL_USER']}:{os.environ['PSWD']}@db:5432/{os.environ['DB']}",
    )
    app.template_folder = template_folder_path
    app._static_folder = static_folder_path
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .views import view
    app.register_blueprint(view, prefix="/")

    return app