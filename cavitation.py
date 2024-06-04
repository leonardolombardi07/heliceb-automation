from typing import Literal
import math


def get_cavitation_evaluation(
        T_delivered: float,  # kN
        T: float,  # m
        n: float,  # rpm
        d: float,  # m
        AeAo: float,
        PD: float,
        Va: float,  # m/s
        rho: float,  # kg/m^3
) -> Literal['ok', 'not ok']:
    # TODO: use Burrill's cavitation diagram values to deal with different cavitation limits. Currently, we are using a heuristical approach for 5% of cavitation limit
    Ao = math.pi*((d**2)/4)
    Ae = Ao*AeAo
    Ap = Ae*(1.067-(0.229*PD))
    vr = ((Va**2)+(0.7*math.pi*d*n)**2)**0.5
    qt = (0.5*rho*(vr**2))
    popv = 101325 - 2278 + \
        (rho*9.805*(T)-((d/2)+0.15))
    sigma = float((popv)/qt)
    tau = float((T_delivered/Ap)/(qt/1000))
    # AeAo = 0,1082*ln(PD)+0,2675 p 5% de cavitacao
    tauregression = 0.1082*math.log(sigma)+0.2675
    sigmaregression = math.exp((tau-0.2675)/0.1082)

    # Heuristical values for 5% of cavitation limit
    if (sigma >= sigmaregression and sigma <= 1.5 and sigma >= 0.16) and (tau <= tauregression and tau <= 0.32 and tau >= 0.08):
        return "ok"
    else:
        return "not ok"
