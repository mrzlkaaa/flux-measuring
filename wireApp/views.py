from flask import render_template, Blueprint
from .model import *

view = Blueprint('view', __name__)
@view.route("/", methods=["GET", "POST"])
def add_sample():
    Experiment.query.all()
    return render_template("add-sample.html")