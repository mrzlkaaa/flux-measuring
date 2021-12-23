import pytest
import requests
from datetime import datetime
from detectorsApp import handler, create_app
from detectorsApp.models import db, Foil_Experiments, Foil_Samples

@pytest.fixture
def client():
    flask_app = create_app({'TESTING': True})
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client

def test_activity():
    A, mass, cool_time, meas_time = handler.activity(net_counts="4023", 
        irr_time=1200, irr_fn=datetime.fromisoformat("2021-04-09 11:39:00"),
        meas_time="30",cool_fn="2021-04-09 11:39:00",
        mass="0.224", foil_type="CU-63")
    assert type(A) == float
    assert type(cool_time) == float
    assert type(meas_time) == float
    assert A > 0

def test_reaction_rate():
    rate, cool_time, meas_time = handler.reaction_rate(net_counts="4023", 
        irr_time=1200, irr_fn=datetime.fromisoformat("2021-04-09 11:39:00"),
        meas_time="30",cool_fn="2021-04-09 11:39:00",
        nucleus_number="9.88E18", foil_type="AU-197")
    assert type(rate) == float
    assert type(cool_time) == float
    assert type(meas_time) == float
    assert 1E-14 < rate > 1E-15

#* test case is when bare and Cd lists aren't empty
def test_ratios_and_thfluxes(client, id=7):
    cd_instances = Foil_Samples.query.filter(
        Foil_Samples.exp_id==id, 
        Foil_Samples.cadmium_filter==True).all()  
    bare_instances = Foil_Samples.query.filter(
        Foil_Samples.exp_id==id, 
        Foil_Samples.cadmium_filter==False).all()
    cd_ratio, th_flux = handler.ratios_and_thfluxes(foil_type="AU-197", 
        cd=cd_instances, 
        bare=bare_instances)
    assert type(cd_ratio) == str
    assert type(th_flux) == str

def test_ratios_and_thfluxes_dispay1(client, id=2):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
    cd_ratio, th_flux, cd_ratios, th_fluxes = handler.ratios_and_thfluxes_display( 
        cd=exper_instance.cd_ratio, 
        th_flux=exper_instance.th_flux)
    assert type(cd_ratio) == float
    assert type(th_flux) == float

def test_ratios_and_thfluxes_dispay2(client, id=1):
    cd_ratio, th_flux, cd_ratios, th_fluxes = handler.ratios_and_thfluxes_display( 
        cd="", 
        th_flux="")
    assert type(cd_ratio) == int
    assert type(th_flux) == int
    assert len(cd_ratios) == 1
    assert len(th_fluxes) == 1

#* test case when cd_ratio EXISTS
def test_ratios_and_thfluxesCD(client, id=10):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()
    cd_instances = Foil_Samples.query.filter(
        Foil_Samples.exp_id==id, 
        Foil_Samples.cadmium_filter==True).all()  
    bare_instances = Foil_Samples.query.filter(
        Foil_Samples.exp_id==id, 
        Foil_Samples.cadmium_filter==False).all()
    if len(cd_instances) == 0 and exper_instance.cd_ratio is not None:
        cd_instances = exper_instance.cd_ratio.split(",")
    cd_ratio, th_flux = handler.ratios_and_thfluxes(foil_type="AU-197", 
        cd=cd_instances, 
        bare=bare_instances)
    assert type(cd_ratio) == str
    assert type(th_flux) == str

#* test case when only cd list is empy and there is NO cd_ratio
def test_ratios_and_thfluxesNoCD(client, id=8):
    exper_instance = Foil_Experiments.query.filter(Foil_Experiments.id==id).first()  
    add_sub_instance = Foil_Samples(name="3CU/200", nucleus_number=1.59E20, 
                            cooling_finished="12/21/2021  1:40:00 PM", area=10873, 
                            cooling_time=60360, measuring_time=300, reaction_rate=2.02E15, 
                            cadmium_filter=False, expermt=exper_instance)
    db.session.add(add_sub_instance)
    db.session.flush()
    cd_instances = Foil_Samples.query.filter(
        Foil_Samples.exp_id==id, 
        Foil_Samples.cadmium_filter==True).all()
    bare_instances = Foil_Samples.query.filter(
        Foil_Samples.exp_id==id, 
        Foil_Samples.cadmium_filter==False).all()
    cd_ratio, th_flux = handler.ratios_and_thfluxes(foil_type="AU-197", 
        cd=cd_instances, 
        bare=bare_instances)
    assert type(cd_ratio) == int
    assert type(th_flux) == int