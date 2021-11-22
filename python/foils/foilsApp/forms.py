from wtforms import Form, StringField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class AddFoil(Form):
    nuclide = StringField("nuclide", validators=[DataRequired()])
    cross_section = DecimalField("cross-section", validators=[DataRequired(), NumberRange(min=0, max=None)])
    abundance = DecimalField("abundance", validators=[DataRequired(), NumberRange(min=0, max=None)])
    half_life = DecimalField("half-life", validators=[DataRequired(), NumberRange(min=0, max=None)])
    energy = StringField("energy", validators=[DataRequired(), NumberRange(min=0, max=None)])
    release = DecimalField("release", validators=[DataRequired(), NumberRange(min=0, max=None)])
    resonance = DecimalField("resonance")
    endf_data = StringField("endf_data")
