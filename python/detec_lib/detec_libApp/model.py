from . import db

class FoilsStore(db.Model):
    __tablename__ = "foils_store"
    id = db.Column(db.Integer, primary_key=True)
    nuclide =  db.Column(db.String(100), nullable=False, unique=True)
    cross_section = db.Column(db.Float(), nullable=False)
    abundance = db.Column(db.Float(), nullable=False)
    half_life = db.Column(db.Float(), nullable=False)
    energy = db.Column(db.String(150), nullable=False)
    release = db.Column(db.String(150), nullable=False)
    resonance = db.Column(db.Float(), nullable=False)
    endf_data = db.Column(db.String(300), nullable=True)
    foils = db.relationship("FoilData", backref="foil_params")

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.id}>"

class FoilData(db.Model):
    __tablename__ = "foil_data"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    nucleus_number = db.Column(db.Float(), nullable=False)
    foil_type = db.Column(db.String, db.ForeignKey("foils_store.nuclide"))

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.id}>"