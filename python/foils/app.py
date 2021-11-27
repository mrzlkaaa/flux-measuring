import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+pg8000://{os.environ['PSQL_USER']}:{os.environ['PSWD']}@{os.environ['HOST']}:{os.environ['PORT']}/actdetectors"


class Experiments(db.Model):
    __tablename__ = "experiments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date = db.Column(db.Date(), default=func.current_date())
    irradiation_finished = db.Column(db.DateTime(), default=func.now())
    irradiation_time = db.Column(db.Float)
    power = db.Column(db.Float)
    foil_type = db.Column(db.String(20))
    samples = db.relationship('Samples', backref='expermt')

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}>"
    
class Samples(db.Model):
    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, default=0)
    cooling_finished = db.Column(db.DateTime())
    area = db.Column(db.Float)
    cooling_time = db.Column(db.Float)
    measuring_time = db.Column(db.Float)
    reaction_rate = db.Column(db.Float)
    cadmium_filter = db.Column(db.Boolean)
    exp_id = db.Column(db.Integer, db.ForeignKey("experiments.id"))

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.id}>"


@app.route("/")
def home():
    return "home"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)