import math
import requests
import json
from datetime import datetime
from collections import defaultdict
from statistics import mean, StatisticsError

det_efficiency = lambda x: 7.50E+00*pow(x,-8.19E-01)
conver_datetime = lambda x: datetime.fromisoformat(x)


detector_params = lambda x: requests.get(f"http://localhost:8080/api/detector_params/nuclide/{x}").json()

# Na = 0.602
# CU = {
#     "M": 62.9296,
#     "E": 511,
#     "Release": 0.343,
#     "Abundance": 0.6917,
#     "Cross-Section":4.51,
#     "Half-Life": 12.701*3600,
# }

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

def rates_and_thflux(*args, **kwargs):
    rate_flux = {"aver": None, "seq": None, "status": False}
    response = detector_params(kwargs["foil_type"])
    cd, bare = kwargs["cd"], kwargs["bare"]
    try:
        aver_cd_rate, aver_bare_rate  = mean([i.reaction_rate for i in cd]), mean([i.reaction_rate for i in bare])
        aver_cd_ratio = aver_bare_rate/aver_cd_rate
        cd_ratio = [i.reaction_rate/aver_cd_rate for i in bare]
        aver_th_flux = (aver_cd_ratio-1)*aver_bare_rate/(response["Cross_section"]*1E-24*aver_cd_ratio)
        thflux = [(i-1)*j/(response["Cross_section"]*1E-24*i) for i,j in zip(cd_ratio, [i.reaction_rate for i in bare])]
        rate_flux["aver"], rate_flux["seq"] = (aver_cd_ratio, aver_th_flux), tuple(zip(cd_ratio, thflux))
        print(rate_flux["seq"])
        rate_flux["status"] = True
    except StatisticsError as e:
        print(e)
        # rate_flux = False
    return rate_flux