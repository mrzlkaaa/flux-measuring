import xlsxwriter
import os
import time
import requests
from flask import render_template, redirect, url_for, Blueprint, request, send_from_directory, flash
from datetime import timedelta, datetime
from . import create_app, template_prefix
from .models import db, Foil_Experiments, Foil_Samples
from .handler import *
from collections import defaultdict
from statistics import mean

foil = Blueprint('foil', __name__)

app = create_app()

@foil.route('/add_foil_experiment', methods=["GET", "POST"])
def add_foil_experiment():
    if request.method == "POST":
        name = request.form["Experiment"]
        irr_time  = (conver_datetime(request.form["Irr-finished"]) - conver_datetime(request.form["Irr-started"])).total_seconds()
        date = conver_datetime(request.form["Irr-finished"]).date()
        print(request.form.get("Cd-ratio"))
        if len(request.form.get("Cd-ratio")) == 0:
            cd_ratio = ""
            print("None is there")
        else:
            cd_ratio = request.form.get("Cd-ratio")
            print("str")
        print(cd_ratio)
        instance = Foil_Experiments(name=name, date=date, irradiation_finished=request.form["Irr-finished"], 
                                    irradiation_time=irr_time, power=1, cd_ratio=cd_ratio, foil_type=request.form["Foil-type"])
        db.session.add(instance)
        db.session.commit()
        return redirect(url_for("foil.foil_experiments_list"))
    return render_template(f"{template_prefix}/add-foil-experiment.html")

@foil.route("/list_foil_experiments", methods=["GET"])
def foil_experiments_list():
    listed = Foil_Experiments.query.all()
    for i in listed:
        try:
            i.cd_ratio = mean([float(j) for j in i.cd_ratio.split(",")])
            i.th_flux = mean([float(j) for j in i.th_flux.split(",")])
            print(i.th_flux)
        except Exception as e:
            print(e)
            i.cd_ratio = 0
            i.th_flux = 0
    return render_template(f"{template_prefix}/list-foil-experiments.html", list=listed)

@foil.route("/foil_experiment/<int:id>", methods=["GET", "POST"])
def detail_foil_experiment(id):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
    irr_fn = exper_instance.irradiation_finished
    print(irr_fn)
    irr_time = exper_instance.irradiation_time
    print(exper_instance.th_flux)    
    exper_instance.cd_ratio, exper_instance.th_flux, exper_instance.cd_ratios, exper_instance.th_fluxes = ratios_and_thfluxes_display(
        cd=exper_instance.cd_ratio, 
        th_flux=exper_instance.th_flux)                                                      
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
        rate, cool_time, meas_time = reaction_rate(net_counts=request.form["Area"], irr_time=irr_time, irr_fn=irr_fn, 
                                                   meas_time=request.form["Meas-time"],cool_fn=request.form["Cool-finished"],
                                                   nucleus_number=nucleus_number, foil_type=exper_instance.foil_type)
        add_sub_instance = Foil_Samples(name=sample_name, nucleus_number=nucleus_number, 
                                        cooling_finished=request.form["Cool-finished"], area=request.form["Area"], 
                                        cooling_time=cool_time, measuring_time=meas_time, reaction_rate=rate, 
                                        cadmium_filter=fltr, expermt=exper_instance)
        db.session.add(add_sub_instance)
        db.session.flush()
        cd_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==True).all()
        bare_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==False).all()
        print(len(bare_instances))
        if len(cd_instances) == 0 and len(bare_instances) > 0:
            cd_instances = ",".join([str(i) for i in exper_instance.cd_ratios])
        exper_instance.cd_ratio, exper_instance.th_flux = ratios_and_thfluxes(foil_type=exper_instance.foil_type, 
                cd=cd_instances, 
                bare=bare_instances)
        # print(exper_instance)
        db.session.commit()
        return redirect(url_for("foil.detail_foil_experiment", id=id))
    return render_template(f"{template_prefix}/foil-experiment.html", data=exper_instance)

@foil.route("/edit_foil_experiment/<int:id>", methods=["GET", "POST"])
def edit_foil_experiment(id):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
    started_time = exper_instance.irradiation_finished - timedelta(seconds=exper_instance.irradiation_time)
    if request.method == "POST":
        exper_instance.name, exper_instance.irradiation_finished = request.form["Experiment"], request.form["Irr-finished"]
        exper_instance.irradiation_time = (conver_datetime(request.form["Irr-finished"]) - conver_datetime( request.form["Irr-started"])).total_seconds()
        exper_instance.date, exper_instance.foil_type = conver_datetime(request.form["Irr-finished"]).date(), request.form["Foil-type"]
        exper_instance.cd_ratio = request.form.get("Cd-ratio")
        db.session.commit()
        return redirect(url_for("foil.detail_foil_experiment", id=id))
    return render_template(f"{template_prefix}/edit-foil-experiment.html", data=exper_instance, irradiation_started=started_time)

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
        exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
        irr_fn = exper_instance.irradiation_finished
        irr_time = exper_instance.irradiation_time
        rate, cool_time, meas_time = reaction_rate(net_counts=request.form["Area"], irr_time=irr_time, irr_fn=irr_fn, 
                                                   meas_time=request.form["Meas-time"],cool_fn=request.form["Cool-finished"],
                                                   nucleus_number=nucleus_number, foil_type=exper_instance.foil_type)
        sample_instance.cooling_finished, sample_instance.area, sample_instance.cooling_time = request.form["Cool-finished"], request.form["Area"], cool_time
        sample_instance.measuring_time, sample_instance.cadmium_filter, sample_instance.reaction_rate = meas_time, fltr, rate
        sample_instance.name = sample_name
        db.session.flush()
        cd_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==True).all()
        bare_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==False).all()
        print(exper_instance.th_flux)
        if len(cd_instances) == 0 and len(bare_instances) > 0:
            cd_instances = exper_instance.cd_ratio
        exper_instance.cd_ratio, exper_instance.th_flux = ratios_and_thfluxes(foil_type=exper_instance.foil_type, 
                cd=cd_instances, 
                bare=bare_instances)
        print(exper_instance.th_flux)
        db.session.commit()
        return redirect(url_for("foil.detail_foil_experiment", id=id))
    return render_template(f"{template_prefix}/edit-foil-sample.html", parent=exper_instance, data=sample_instance)

@foil.route("/<int:id>/export", methods=["GET","POST"])
def export_foil_experiment(id):
    if request.method == "POST":
        dct = defaultdict(list)
        instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
        dct['irradiation_finished'].append(instance.irradiation_finished)
        dct['irradiation_time'].append(instance.irradiation_time)
        for n, i in enumerate(instance.samples):
            dct["name"].append(i.name)
            dct["nucleus_number"].append(i.nucleus_number)
            dct["cooling_finished"].append(i.cooling_finished)
            dct["cooling_time"].append(i.cooling_time)
            dct["measuring_time"].append(i.measuring_time)
            dct["cadmium_filter"].append(i.cadmium_filter)
            dct["area"].append(i.area)
            dct["reaction_rate"].append(i.reaction_rate)
        try:
            os.mkdir(os.path.join(os.getcwd(), "Downloads"))
        except FileExistsError as e:
            print(e)
        file_name = f"export_foil_{instance.name}.xlsx"
        with xlsxwriter.Workbook(os.path.join(app.config["DOWNLOAD_FOLDER"], file_name)) as wb:
            wsh = wb.add_worksheet()
            header = ["IrrFinished", "IrrTime", "Name", "Nucleus", "CoolFinished", "CoolTime", "MeasTime", "CadFilter", "NetCounts", "ReactionRate"]
            header_format = wb.add_format({ 'bold': True,
                                            'bottom': 2,
                                            'bg_color': '#F9DA04'})
            datetime_format = wb.add_format({'num_format': 'dd/mm/yy hh:mm'})
            for n, i in enumerate(header, start=1):
                wsh.write(1, n, i, header_format)
            for num, i in enumerate(dct.values(), start=1):
                if not isinstance(i[0], datetime):
                    wsh.write_column(2, num, i)
                else:
                    wsh.write_column(2, num, i, datetime_format)
        return send_from_directory(app.config["DOWNLOAD_FOLDER"], file_name, as_attachment=True)

@foil.route("/<int:id>/fedelete", methods=["GET","POST"])
def delete_foil_experiment(id):
    if request.method == "POST":
        instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
        db.session.delete(instance)
        print(instance)
        db.session.commit()
        return redirect(url_for("foil.foil_experiments_list"))

@foil.route("/<int:id>/<int:sample_id>/fsdelete", methods=["GET","POST"])
def delete_foil_sample(id, sample_id):
    if request.method == "POST":
        sample_instance = Foil_Samples.query.join(Foil_Experiments).filter(Foil_Experiments.id==id, Foil_Samples.id==sample_id).first()
        print(sample_instance)
        db.session.delete(sample_instance)
        exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
        cd_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==True).all()
        bare_instances = Foil_Samples.query.filter(Foil_Samples.exp_id==id, Foil_Samples.cadmium_filter==False).all()
        if len(cd_instances) == 0 and len(bare_instances) > 0:
            cd_instances = exper_instance.cd_ratio
        exper_instance.cd_ratio, exper_instance.th_flux = ratios_and_thfluxes(foil_type=exper_instance.foil_type, 
                cd=cd_instances, 
                bare=bare_instances)
        print(sample_instance)
        db.session.commit()
        return redirect(url_for("foil.detail_foil_experiment", id=id))