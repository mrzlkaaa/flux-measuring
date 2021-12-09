# import redis
from . import db
from sqlalchemy import func

# r = redis.Redis(host="redis", port = "6379", db=0)
# r = redis.Redis(host="localhost", port = "6379", db=0)

class Experiment(db.Model):
    __tablename__ = "experiment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date = db.Column(db.Date(), default=func.current_date())
    irradiation_finished = db.Column(db.DateTime(), default=func.now())
    irradiation_time = db.Column(db.Float)
    power = db.Column(db.Float)
    foil_type = db.Column(db.String(20))
    samples = db.relationship('Sample', backref='expermt')

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}>"
    
class Sample(db.Model):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, default=0)
    cooling_finished = db.Column(db.DateTime())
    area = db.Column(db.Float)
    cooling_time = db.Column(db.Float)
    measuring_time = db.Column(db.Float)
    mass = db.Column(db.Float)
    activity = db.Column(db.Float)
    exp_id = db.Column(db.Integer, db.ForeignKey("experiment.id"))

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}>"

class Foil_Experiments(db.Model):
    __tablename__ = "foil_experiments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    date = db.Column(db.Date(), default=func.current_date())
    irradiation_finished = db.Column(db.DateTime(), default=func.now())
    irradiation_time = db.Column(db.Float)
    cd_ratio = db.Column(db.Text)
    th_flux = db.Column(db.Text)
    power = db.Column(db.Float)
    foil_type = db.Column(db.String(20))
    samples = db.relationship('Foil_Samples', backref='expermt')

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.name}>"
    
class Foil_Samples(db.Model):
    __tablename__ = 'foil_samples'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    nucleus_number = db.Column(db.Float)
    cooling_finished = db.Column(db.DateTime())
    area = db.Column(db.Float)
    cooling_time = db.Column(db.Float)
    measuring_time = db.Column(db.Float)
    reaction_rate = db.Column(db.Float)
    cadmium_filter = db.Column(db.Boolean)
    exp_id = db.Column(db.Integer, db.ForeignKey("foil_experiments.id"))

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.id}>"