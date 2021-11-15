import xlsxwriter
import os
from flask import render_template, redirect, url_for, Blueprint, request, send_from_directory
from datetime import timedelta
from . import create_app
from .model import *
from .handler import *
from collections import defaultdict

view = Blueprint('view', __name__)

app = create_app()

@view.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["Experiment"]
        irr_time  = (conver_datetime(request.form["Irr-finished"]) - conver_datetime( request.form["Irr-started"])).total_seconds()
        instance = Experiment(name=name, irradiation_finished=request.form["Irr-finished"], irradiation_time=irr_time, power=1)
        db.session.add(instance)
        db.session.commit()
        return redirect(url_for("view.experiments_list"))
    return render_template("add-experiment.html")

@view.route("/list", methods=["GET"])
def experiments_list():
    listed = Experiment.query.all()
    return render_template("list.html", list=listed)


@view.route("/experiment/<name>", methods=["GET", "POST"])
def detail(name):
     #f"/{name}")  #* pass name of instance to  make urlpath and prepare api.py
    exper_instance = Experiment.query.filter(Experiment.name==name).first()
    r.set("api_ID", exper_instance.id)
    irr_fn = exper_instance.irradiation_finished
    irr_time = exper_instance.irradiation_time
    if request.method == "POST":
        id = request.form["Id"]
        print(type(id))
        A, mass, cool_time, meas_time = activity(net_counts=request.form["Area"], irr_time=irr_time, irr_fn=irr_fn, meas_time=request.form["Meas-time"],
                                            cool_fn=request.form["Cool-finished"], mass=request.form["Mass"])
        print(A)
        add_sub_instance = Sample(id=id, cooling_finished=request.form["Cool-finished"], area=request.form["Area"], 
                                activity=A, cooling_time=cool_time, measuring_time=meas_time, mass=mass, expermt=exper_instance)
        # db.session.add(add_sub_instance)
        # db.session.commit()
        return redirect(url_for("view.detail", name=name))
    return render_template("experiment.html", data=exper_instance)

@view.route("/edit/<name>", methods=["GET", "POST"])
def edit_experiment(name):
    exper_instance = Experiment.query.filter(Experiment.name==name).first()
    started_time = exper_instance.irradiation_finished - timedelta(seconds=exper_instance.irradiation_time)
    if request.method == "POST":
        exper_instance.name, exper_instance.irradiation_finished = request.form["Experiment"], request.form["Irr-finished"]
        exper_instance.irradiation_time = (conver_datetime(request.form["Irr-finished"]) - conver_datetime( request.form["Irr-started"])).total_seconds()
        db.session.commit()
        return redirect(url_for("view.detail", name=name))
    return render_template("edit-experiment.html", data=exper_instance, irradiation_started=started_time)

@view.route("/edit/<name>/<sample_id>/", methods=["GET", "POST"])
def edit_sample(name, sample_id):
    sample_instance = Sample.query.join(Experiment).filter(Experiment.name==name, Sample.id==int(sample_id)).first()
    print(sample_instance.cooling_finished)
    if request.method == "POST":
        exper_instance = Experiment.query.filter(Experiment.name==name).first()
        irr_fn = exper_instance.irradiation_finished
        irr_time = exper_instance.irradiation_time
        A, mass, cool_time, meas_time = activity(net_counts=request.form["Area"], irr_time=irr_time, irr_fn=irr_fn, meas_time=request.form["Meas-time"],
                                                 cool_fn=request.form["Cool-finished"], mass=request.form["Mass"])
        sample_instance.cooling_finished, sample_instance.area, sample_instance.cooling_time = request.form["Cool-finished"], request.form["Area"], cool_time
        sample_instance.measuring_time, sample_instance.mass, sample_instance.activity = meas_time, mass, A
        db.session.flush()
        db.session.commit()
        return redirect(url_for("view.detail", name=name))
    return render_template("edit-sample.html", data=sample_instance)

@view.route("/<name>/export", methods=["GET","POST"])
def export_experiment(name):
    if request.method == "POST":
        dct = defaultdict(list)
        instance = Experiment.query.filter(Experiment.name==name).first()
        dct['irradiation_finished'].append(instance.irradiation_finished)
        dct['irradiation_time'].append(instance.irradiation_time)
        for n, i in enumerate(instance.samples):
            dct["id"].append(i.id)
            dct["cooling_finished"].append(i.cooling_finished)
            dct["cooling_time"].append(i.cooling_time)
            dct["measuring_time"].append(i.measuring_time)
            dct["mass"].append(i.mass)
            dct["area"].append(i.area)
            dct["activity"].append(i.activity)
        try:
            os.mkdir(os.path.join(os.getcwd(), "Downloads"))
        except FileExistsError as e:
            print(e)
        with xlsxwriter.Workbook(os.path.join(app.config["DOWNLOAD_FOLDER"], "export.xlsx")) as wb:
            wsh = wb.add_worksheet()
            header = ["IrrFinished", "IrrTime", "ID", "CoolFinished", "CoolTime", "MeasTime", "Mass", "NetCounts", "Activity"]
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
        return send_from_directory(app.config["DOWNLOAD_FOLDER"], "export.xlsx", as_attachment=True)

@view.route("/<name>/delete", methods=["GET","POST"])
def delete_experiment(name):
    if request.method == "POST":
        instance = Experiment.query.filter(Experiment.name==name).first()
        db.session.delete(instance)
        print(instance)
        db.session.commit()
        return redirect(url_for("view.experiments_list"))