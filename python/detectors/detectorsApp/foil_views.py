import xlsxwriter
import os
import time
import requests
from flask import render_template, redirect, url_for, Blueprint, request, send_from_directory
from datetime import timedelta
from . import create_app, template_prefix
from .models import db, Foil_Experiments, Foil_Samples
from .handler import reaction_rate, conver_datetime, rates_and_thflux
from collections import defaultdict

foil = Blueprint('foil', __name__)

app = create_app()

@foil.route('/add_foil_experiment', methods=["GET", "POST"])
def add_foil_experiment():
    if request.method == "POST":
        name = request.form["Experiment"]
        irr_time  = (conver_datetime(request.form["Irr-finished"]) - conver_datetime(request.form["Irr-started"])).total_seconds()
        date = conver_datetime(request.form["Irr-finished"]).date()
        instance = Foil_Experiments(name=name, date=date, irradiation_finished=request.form["Irr-finished"], 
                              irradiation_time=irr_time, power=1, foil_type=request.form["Foil-type"])
        db.session.add(instance)
        db.session.commit()
        return redirect(url_for("foil.foil_experiments_list"))
    return render_template(f"{template_prefix}/add-foil-experiment.html")

@foil.route("/list_foil_experiments", methods=["GET"])
def foil_experiments_list():
    listed = Foil_Experiments.query.all()
    return render_template(f"{template_prefix}/list-foil-experiments.html", list=listed)

@foil.route("/foil_experiment/<int:id>", methods=["GET", "POST"])
def detail_foil_experiment(id):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
    irr_fn = exper_instance.irradiation_finished
    irr_time = exper_instance.irradiation_time
    cd_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==True).all()
    bare_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==False).all()
    rate_flux = rates_and_thflux(foil_type=exper_instance.foil_type, cd=cd_instances, 
                                                                     bare=bare_instances)                                                                   
    if request.method == "POST":
        try:
            value = request.form["filter"]
            fltr = True
        except KeyError:
            print("error")
            fltr = False
        sample_name, nucleus_number = request.form["Name"].split("-")
        rate, cool_time, meas_time = reaction_rate(net_counts=request.form["Area"], irr_time=irr_time, irr_fn=irr_fn, 
                                                   meas_time=request.form["Meas-time"],cool_fn=request.form["Cool-finished"],
                                                   nucleus_number=nucleus_number, foil_type=exper_instance.foil_type)
        add_sub_instance = Foil_Samples(name=sample_name, nucleus_number=nucleus_number, 
                                        cooling_finished=request.form["Cool-finished"], area=request.form["Area"], 
                                        cooling_time=cool_time, measuring_time=meas_time, reaction_rate=rate, 
                                        cadmium_filter=fltr, expermt=exper_instance)
        db.session.add(add_sub_instance)
        db.session.flush()
        db.session.commit()
        return redirect(url_for("foil.detail_foil_experiment", id=id))
    return render_template(f"{template_prefix}/foil-experiment.html", data=exper_instance, 
                           rate_flux = rate_flux)

@foil.route("/edit_foil_experiment/<int:id>", methods=["GET", "POST"])
def edit_foil_experiment(id):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
    started_time = exper_instance.irradiation_finished - timedelta(seconds=exper_instance.irradiation_time)
    if request.method == "POST":
        exper_instance.name, exper_instance.irradiation_finished = request.form["Experiment"], request.form["Irr-finished"]
        exper_instance.irradiation_time = (conver_datetime(request.form["Irr-finished"]) - conver_datetime( request.form["Irr-started"])).total_seconds()
        exper_instance.date, exper_instance.foil_type = conver_datetime(request.form["Irr-finished"]).date(), request.form["Foil-type"]
        db.session.commit()
        return redirect(url_for("foil.detail_foil_experiment", id=id))
    return render_template(f"{template_prefix}/edit-wire-experiment.html", data=exper_instance, irradiation_started=started_time)

@foil.route("/edit_foil_experiment/<int:id>/<int:sample_id>", methods=["GET", "POST"])
def edit_foil_sample(id, sample_id):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
    sample_instance = Foil_Samples.query.join(Foil_Experiments).filter(Foil_Experiments.id==id, 
                                                                       Foil_Samples.id==sample_id).first()
    if request.method == "POST":
        try:
            value = request.form["filter"]
            fltr = True
        except KeyError:
            print("error")
            fltr = False
        except Exception as e:
            print(e)
        sample_name, nucleus_number = request.form["Name"].split("-")
        print(sample_name, nucleus_number)
        exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==int(id)).first()
        irr_fn = exper_instance.irradiation_finished
        irr_time = exper_instance.irradiation_time
        rate, cool_time, meas_time = reaction_rate(net_counts=request.form["Area"], irr_time=irr_time, irr_fn=irr_fn, 
                                                   meas_time=request.form["Meas-time"],cool_fn=request.form["Cool-finished"],
                                                   nucleus_number=nucleus_number, foil_type=exper_instance.foil_type)
        sample_instance.cooling_finished, sample_instance.area, sample_instance.cooling_time = request.form["Cool-finished"], request.form["Area"], cool_time
        sample_instance.measuring_time, sample_instance.cadmium_filter, sample_instance.reaction_rate = meas_time, fltr, rate
        sample_instance.name = sample_name
        db.session.flush()
        db.session.commit()
        return redirect(url_for("foil.detail_foil_experiment", id=id))
    return render_template(f"{template_prefix}/edit-foil-sample.html", parent=exper_instance, data=sample_instance)

# @foil.route("/<name>/export", methods=["GET","POST"])
# def export_wire_experiment(name):
#     if request.method == "POST":
#         dct = defaultdict(list)
#         instance = Experiment.query.filter(Experiment.name==name).first()
#         dct['irradiation_finished'].append(instance.irradiation_finished)
#         dct['irradiation_time'].append(instance.irradiation_time)
#         for n, i in enumerate(instance.samples):
#             dct["id"].append(i.id)
#             dct["cooling_finished"].append(i.cooling_finished)
#             dct["cooling_time"].append(i.cooling_time)
#             dct["measuring_time"].append(i.measuring_time)
#             dct["mass"].append(i.mass)
#             dct["area"].append(i.area)
#             dct["activity"].append(i.activity)
#         try:
#             os.mkdir(os.path.join(os.getcwd(), "Downloads"))
#         except FileExistsError as e:
#             print(e)
#         with xlsxwriter.Workbook(os.path.join(app.config["DOWNLOAD_FOLDER"], "export.xlsx")) as wb:
#             wsh = wb.add_worksheet()
#             header = ["IrrFinished", "IrrTime", "ID", "CoolFinished", "CoolTime", "MeasTime", "Mass", "NetCounts", "Activity"]
#             header_format = wb.add_format({ 'bold': True,
#                                             'bottom': 2,
#                                             'bg_color': '#F9DA04'})
#             datetime_format = wb.add_format({'num_format': 'dd/mm/yy hh:mm'})
#             for n, i in enumerate(header, start=1):
#                 wsh.write(1, n, i, header_format)
#             for num, i in enumerate(dct.values(), start=1):
#                 if not isinstance(i[0], datetime):
#                     wsh.write_column(2, num, i)
#                 else:
#                     wsh.write_column(2, num, i, datetime_format)
#         return send_from_directory(app.config["DOWNLOAD_FOLDER"], "export.xlsx", as_attachment=True)

# @foil.route("/<id>/delete", methods=["GET","POST"])
# def delete_wire_experiment(name):
#     if request.method == "POST":
#         instance = Experiment.query.filter(Experiment.id==int(id)).first()
#         db.session.delete(instance)
#         print(instance)
#         db.session.commit()
#         return redirect(url_for("wire.wire_experiments_list"))

# @foil.route("/<id>/<sample_id>/delete", methods=["GET","POST"])
# def delete_wire_sample(id, sample_id):
#     if request.method == "POST":
#         sample_instance = Sample.query.join(Experiment).filter(Experiment.id==int(id), Sample.name==int(sample_id)).first()
#         db.session.delete(sample_instance)
#         print(sample_instance)
#         db.session.commit()
#         return redirect(url_for("wire.wire_experiments_list"))