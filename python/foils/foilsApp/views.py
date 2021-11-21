from flask import request, render_template, Blueprint
from .forms import AddFoil
from .model import *


view = Blueprint('view', __name__)


@view.route("/add-foil", methods = ['GET', 'POST'])
def add_foil():
    all = FoilsStore.query.all()
    print(all)
    form = AddFoil()
    print(form.nuclide.data)
    if request.method == "POST":
        new = FoilsStore(nuclide=request.form.get("nuclide").upper(), cross_section=request.form.get("cross_section"), 
                         abundance=request.form.get("abundance"), half_life=request.form.get("half_life"), 
                         energy=request.form.get("energy"), resonance=request.form.get("resonance"))
        print(new)
        db.session.add(new)
        db.session.commit()
    return render_template("foilsApp/add-foil.html", form=form)


@view.route("/foils-store", methods=["GET", "POST"])
def foils_store():
    return render_template("foilsApp")