# External imports
from typing import Literal
from math import log, pi


def get_cavitation_evaluation(
        rho: float,  # Water density, kg/m^3
        Pa: float,  # Atmospheric pressure, Pa
        Ps: float,  # Pressure of saturation of water, Pa
        g: float,  # Acceleration of gravityon earth's surface, m/s^2

        T: float,  # Ship draft at front perpendicular, m
        d: float,  # propeller diameter, m
        T_delivered: float,  # kN

        shaft_depth: float,  # m
        Va: float,  # Advance velocity, m/s. It seems that Vs is used on the spreadsheet though

        PD: float,  # Pitch/Diameter ratio
        AeAo: float,  # Area ratio
        n: float,  # propeller rotation, rpm

        cavitation_limit: float,  # cavitation in limit, as percentage
) -> Literal['ok', 'not ok']:
    V_07_R_squared = (Va**2) + (pi * n * 0.7 * d)**2  # m/s

    P_dynamic = 0.5 * V_07_R_squared * rho  # Pa
    P_static = (Pa - Ps) + rho * g * T  # Pa

    sigma_07_R = P_static / P_dynamic

    Ao = pi * (d**2) / 4  # m2
    Ae = Ao * AeAo  # m2
    Ap = Ae * (1.067 - 0.229*PD)  # m2 (Ad =~ Ae)

    tau_c = (T_delivered * 1000) / (0.5*rho*V_07_R_squared*Ap)

    tauc_max: float = 0
    if shaft_depth <= 0.025:
        tauc_max = 0.09798 * log(sigma_07_R) + 0.23426
    elif shaft_depth > 0.05:
        tauc_max = 0.14093 * log(sigma_07_R) + 0.3458
    else:
        tauc_max = 0.11104 * log(sigma_07_R) + 0.27104

    delta_tauc = (tauc_max/tau_c) - 1

    return "ok" if delta_tauc > cavitation_limit else "not ok"
