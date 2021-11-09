from . import db
from sqlalchemy import func


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date = db.Column(db.Date(), default=func.current_date())
    irradiation_time = db.Column(db.Float)
    power = db.Column(db.Float)
    samples = db.relationship('Sample')

    def __repr__(self):
        return f"{self.__name__}<{self.id}>"
    
class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cooling_time = db.Column(db.Float)
    measuring_time = db.Column(db.Float)
    activity = db.Column(db.Float)
    exper_name = db.Column(db.String(100), db.ForeignKey("experiment.name"))
