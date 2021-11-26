from datetime import datetime
import math
import requests
import json

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
    # cooling. measuring, activity
