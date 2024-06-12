# External imports
from math import sqrt, pi


def get_Re(
    Va: float,  # Advance velocity, m/s. It seems that Vs is used on the spreadsheet though
    n: float,  # propeller rotation, Hz
    d: float,  # propeller diameter, m
    v: float,  # fluid kinematic viscosity, m^2/s
    nblades: int,  # number of blades
    AeAo: float,  # Area ratio
) -> float:
    C_075_R = 2.073 * AeAo * d / nblades
    return C_075_R * sqrt((Va**2) + (0.75*pi*n*d)**2) / v
