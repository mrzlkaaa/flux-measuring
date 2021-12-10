import math
import requests
import json
import itertools
from datetime import datetime
from collections import defaultdict
from statistics import mean, StatisticsError

det_efficiency = lambda x: 7.50E+00*pow(x,-8.19E-01)
conver_datetime = lambda x: datetime.fromisoformat(x)

detector_params = lambda x: requests.get(f"http://109.123.162.90:8080/api/detector_params/nuclide/{x}").json()

def activity(*args, **kwargs):
    response = detector_params(kwargs["foil_type"])
    constant_decay = 0.693/response["Half_life"]
    cool_time = (conver_datetime(kwargs["cool_fn"]) - kwargs["irr_fn"]).total_seconds()
    print(cool_time, kwargs['irr_time'])
    net_counts, meas_time, mass = float(kwargs["net_counts"]), float(kwargs["meas_time"]), float(kwargs["mass"])
    A0 = (constant_decay*net_counts*math.exp(constant_decay*cool_time))/(mass
                *(1-math.exp(-constant_decay*kwargs["irr_time"]))*(1-math.exp(-constant_decay*meas_time))*response["Abundance"]
                *float(response["Release"])*det_efficiency(float(response["Energy"])))
    return A0, mass, cool_time, meas_time

def reaction_rate(*args, **kwargs):
    response = detector_params(kwargs["foil_type"])
    constant_decay = 0.693/response["Half_life"]
    cool_time = (conver_datetime(kwargs["cool_fn"]) - kwargs["irr_fn"]).total_seconds()
    print(cool_time, kwargs['irr_time'])
    net_counts, meas_time = float(kwargs["net_counts"]), float(kwargs["meas_time"])
    rate = (constant_decay*net_counts*math.exp(constant_decay*cool_time))/((1-math.exp(-constant_decay*kwargs["irr_time"]))
                *(1-math.exp(-constant_decay*meas_time))*response["Abundance"]
                *float(response["Release"])*det_efficiency(float(response["Energy"]))
                *float(kwargs["nucleus_number"]))
    return rate, cool_time, meas_time

def ratios_and_thfluxes(*args, **kwargs):
    response = detector_params(kwargs["foil_type"])
    cd, bare = kwargs["cd"], kwargs["bare"]
    try:
        aver_cd_rate = mean([i.reaction_rate for i in cd])
        cd_ratio = [i.reaction_rate/aver_cd_rate for i in bare]
        thflux = [(i-1)*j/(response["Cross_section"]*1E-24*i) for i,j in zip(cd_ratio, [i.reaction_rate for i in bare])]
    except Exception as e:
        print(e)
        cd_ratio = [float(i) for i in cd.split(",")]
        cd_aver = mean(cd_ratio)
        thflux = [((cd_aver-1)*i)/(response["Cross_section"]*1E-24*cd_aver) for i in [i.reaction_rate for i in bare]]
    ratios, th_fluxes = ",".join([str(i) for i in cd_ratio]), ",".join([str(i) for i in thflux])
    return ratios, th_fluxes

def ratios_and_thfluxes_display(*args, **kwargs):
    try:
        cds, th_fluxes = [float(i) for i in kwargs["cd"].split(",")], [float(i) for i in kwargs["th_flux"].split(",")]
        mean_cds, mean_th_fluxes = mean(cds), mean(th_fluxes)
    except Exception as e:
        print(e)
        return 0, 0, [0], [0]
    return mean_cds, mean_th_fluxes, cds, th_fluxes