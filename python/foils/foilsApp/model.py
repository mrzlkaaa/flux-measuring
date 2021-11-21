from . import db

class FoilsStore(db.Model):
    # __tablename__ = "foils_store"
    id = db.Column(db.Integer, primary_key=True)
    nuclide =  db.Column(db.String(100), nullable=False, unique=True)
    cross_section = db.Column(db.Float(), nullable=False)
    abundance = db.Column(db.Float(), nullable=False)
    half_life = db.Column(db.Float(), nullable=False)
    energy = db.Column(db.Float(), nullable=False)
    resonance = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.id}>"