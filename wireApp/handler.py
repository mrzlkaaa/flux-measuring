from datetime import datetime
import math

det_efficiency = lambda x: 7.50E+00*pow(x,-8.19E-01)
conver_datetime = lambda x: datetime.fromisoformat(x)

Na = 0.602
CU = {
    "M": 62.9296,
    "E": 511,
    "Release": 0.343,
    "Abundance": 0.6917,
    "Cross-Section":4.51,
    "Half-Life": 12.701*3600,
}

def activity(*args, **kwargs):
    constant_decay = 0.693/CU["Half-Life"]
    cool_time = (conver_datetime(kwargs["cool_fn"]) - kwargs["irr_fn"]).total_seconds()
    print(cool_time, kwargs['irr_time'])
    net_counts, meas_time, mass = float(kwargs["net_counts"]), float(kwargs["meas_time"]), float(kwargs["mass"])
    A0 = (constant_decay*net_counts*math.exp(constant_decay*cool_time))/(mass
                *(1-math.exp(-constant_decay*kwargs["irr_time"]))*(1-math.exp(-constant_decay*meas_time)))
    return A0, mass, cool_time, meas_time
    # cooling. measuring, activity
