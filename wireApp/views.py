from flask import render_template, Blueprint, request
from .model import *

view = Blueprint('view', __name__)
@view.route("/", methods=["GET", "POST"])
def add_sample():
    if request.method == "POST":
        id = request.form["Id"]
        irr_st = request.form["Irr-started"]
        irr_fn = request.form["Irr-finished"]
        print(type(irr_st))
    return render_template("add-sample.html")