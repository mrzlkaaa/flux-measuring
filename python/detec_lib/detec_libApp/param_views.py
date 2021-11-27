from flask import request, render_template, Blueprint, redirect, url_for
from . import template_prefix
from .forms import AddDetParams
from .model import *


params = Blueprint('params', __name__)

def half_life_converter(key, value):
    value = float(value)
    if key == "s": value = value*1
    elif key == "h": value = value*3600
    elif key == "d": value = value*24*3600
    elif key == "y": value = value*365*24*3600
    return value


@params.route("/add-detector-param", methods = ['GET', 'POST'])
def add_detector_param():
    form = AddDetParams()
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
        return redirect(url_for("view.list_detector_params"))
    return render_template(f"{template_prefix}/add-detector-param.html", form=form)

@params.route("/edit/<nuclide>", methods = ['GET', 'POST'])
def edit_detector_param(nuclide):
    instance = FoilsStore.query.filter(FoilsStore.nuclide==nuclide).first()
    form = AddDetParams()
    form.nuclide.data, form.cross_section.data, form.abundance.data = instance.nuclide, instance.cross_section, instance.abundance
    form.half_life.data, form.energy.data, form.release.data = instance.half_life, instance.energy, instance.release
    form.resonance.data, form.endf_data.data = instance.resonance, instance.endf_data
    if request.method == "POST":
        print(form.nuclide.data, form.endf_data.data)
        half_life = half_life_converter(request.form.get("half_life_type"), request.form.get("half_life"))
        print(half_life)
        instance.nuclide, instance.cross_section = request.form.get("nuclide").upper(), request.form.get("cross_section")
        instance.abundance, instance.half_life = request.form.get("abundance"), half_life
        instance.energy, instance.release = request.form.get("energy"), request.form.get("release")
        instance.resonance, instance.endf_data = request.form.get("resonance"), request.form.get("endf_data")
        db.session.commit()
        return redirect(url_for("view.list_detector_params"))
    return render_template(f"{template_prefix}/edit-detector-param.html", form=form)

@params.route("/list_detector_params", methods=["GET", "POST"])
def list_detector_params():
    listed = FoilsStore.query.all()
    print(listed)
    return render_template(f"{template_prefix}/list-detector-params.html", list=listed)

@params.route("/delete/<nuclide>", methods=["GET", "POST"])
def delete_detector_param(nuclide):
    if request.method == "POST":
        on_delete = FoilsStore.query.filter(FoilsStore.nuclide==nuclide).first()
        db.session.delete(on_delete)
        db.session.commit()
        return redirect(url_for("view.list_detector_params"))