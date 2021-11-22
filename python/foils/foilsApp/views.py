from flask import request, render_template, Blueprint, redirect, url_for
from .forms import AddFoil
from .model import *


view = Blueprint('view', __name__)

def half_life_converter(key, value):
    value = float(value)
    if key == "s": value = value*1
    elif key == "h": value = value*3600
    elif key == "d": value = value*24*3600
    elif key == "y": value = value*365*24*3600
    return value


@view.route("/add-foil-data", methods = ['GET', 'POST'])
def add_foil():
    form = AddFoil()
    if request.method == "POST":
        print(request.form.get("half_life_type"), request.form.get("half_life"))
        half_life = half_life_converter(request.form.get("half_life_type"), request.form.get("half_life"))
        print(half_life)
        new = FoilsStore(nuclide=request.form.get("nuclide").upper(), cross_section=request.form.get("cross_section"), 
                         abundance=request.form.get("abundance"), half_life=half_life, 
                         energy=request.form.get("energy"), release=request.form.get("release"), resonance=request.form.get("resonance"), 
                         endf_data=request.form.get("endf_data"))
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("view.foils_store"))
    return render_template("foilsApp/add-foil-data.html", form=form)

@view.route("/edit/<nuclide>", methods = ['GET', 'POST'])
def edit_foil(nuclide):
    instance = FoilsStore.query.filter(FoilsStore.nuclide==nuclide).first()
    form = AddFoil()
    form.nuclide.data = instance.nuclide
    # if request.method == "POST":
        # print(request.form.get("half_life_type"), request.form.get("half_life"))
        # half_life = half_life_converter(request.form.get("half_life_type"), request.form.get("half_life"))
        # print(half_life)
        # new = FoilsStore(nuclide=request.form.get("nuclide").upper(), cross_section=request.form.get("cross_section"), 
        #                  abundance=request.form.get("abundance"), half_life=half_life, 
        #                  energy=request.form.get("energy"), release=request.form.get("release"), resonance=request.form.get("resonance"), 
        #                  endf_data=request.form.get("endf_data"))
        # db.session.add(new)
        # db.session.commit()
        # return redirect(url_for("view.foils_store"))
    return render_template("foilsApp/edit-foil-data.html", form=form)

@view.route("/foils-data", methods=["GET", "POST"])
def foils_store():
    listed = FoilsStore.query.all()
    print(listed)
    return render_template("foilsApp/foils-data.html", list=listed)