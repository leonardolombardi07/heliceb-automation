# External imports
from math import log10


def _get_delta_kt(
    J: float,
    PD: float,
    AeAo: float,
    nblades: int,
    Re: float,
) -> float:
    c = (log10(Re) - 0.301)

    a1 = 0.000353485
    a2 = -0.00333758 * AeAo * (J**2)
    a3 = -0.00478125 * AeAo * PD * J
    a4 = +0.000257792 * (c**2) * AeAo * (J**2)
    a5 = +0.0000643192 * c * (PD**6) * (J**2)
    a6 = -0.0000110636 * (c**2) * (PD**6) * (J**2)
    a7 = -0.0000276305 * (c**2) * nblades * AeAo * (J ** 2)
    a8 = +0.0000954 * c * nblades * AeAo * PD * J

    # Heads up! Alho's spreadsheet is wrong here
    # It considers c**2 instead of c
    # To keep the same result, we consider c**2 as well
    wrong_c_for_a9 = c**2
    a9 = +0.0000032049 * wrong_c_for_a9 * (nblades**2) * AeAo * (PD**3) * J

    return a1+a2+a3+a4+a5+a6+a7+a8+a9


def _get_kt(
    J: float,
    PD: float,
    AeAo: float,
    nblades: int,
) -> float:
    a1 = (0.00880496000)*1*1*1*1
    a2 = -0.20455400000*J*1*1*1
    a3 = 0.16635100000*PD*1*1*1
    a4 = 0.15811400000*(PD**2)*1*1*1
    a5 = -0.14758100000*(J**2)*(AeAo)*1*1
    a6 = -0.48149700000*(J)*PD*AeAo*1
    a7 = 0.41543700000*(PD**2)*AeAo*1*1
    a8 = (0.01440430000)*nblades*1*1*1
    a9 = -0.05300540000*(J**2)*nblades*1*1
    a10 = 0.01434810000*PD*nblades*1*1
    a11 = 0.06068260000*J*PD*nblades*1
    a12 = -0.01258940000*AeAo*nblades*1*1
    a13 = 0.01096890000*J*nblades*AeAo*1
    a14 = -0.13369800000*(PD**3)*1*1*1
    a15 = 0.00638407000*(PD**6)*1*1*1
    a16 = -0.00132718000*(J**2)*(PD**6)*1*1
    a17 = 0.16849600000*(J**3)*AeAo*1*1
    a18 = -0.05072140000*(AeAo**2)*1*1*1
    a19 = 0.08545590000*(J**2)*(AeAo**2)*1*1
    a20 = -0.05044750000*(J**3)*(AeAo**2)*1*1
    a21 = 0.01046500000*(J)*(PD**6)*(AeAo**2)*1
    a22 = -0.0064827200*(J**2)*(PD**6)*(AeAo**2)*1
    a23 = -0.00841728000*(PD**3)*nblades*1*1
    a24 = 0.01684240000*(J)*(PD**3)*nblades*1
    a25 = -0.00102296000*(J**3)*(PD**3)*nblades*1
    a26 = -0.03177910000*(PD**3)*AeAo*nblades*1
    a27 = 0.01860400000*(J)*(AeAo**2)*nblades*1
    a28 = -0.00410798000*(PD**2)*(AeAo**2)*nblades*1
    a29 = -0.00060684800*(nblades**2)*1*1*1
    a30 = -0.00498190000*(J)*(nblades**2)*1*1
    a31 = 0.00259830000*(J**2)*(nblades**2)*1*1
    a32 = -0.00056052800*(J**3)*(nblades**2)*1*1
    a33 = -0.00163652000*(J)*(PD**2)*(nblades**2)*1
    a34 = -0.00032878700*(J)*(PD**6)*(nblades**2)*1
    a35 = 0.00011650200*(J**2)*(PD**6)*(nblades**2)*1
    a36 = 0.00069090400*(AeAo)*(nblades**2)*1*1
    a37 = 0.00421749000*(PD**3)*AeAo*(nblades**2)*1
    a38 = 0.00005652229*(J**3)*(PD**6)*AeAo*(nblades**2)
    a39 = -0.00146564000*(PD**3)*(AeAo**2)*(nblades**2)*1

    kt = a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12+a13+a14+a15+a16+a17+a18+a19+a20 + \
        a21+a22+a23+a24+a25+a26+a27+a28+a29+a30+a31+a32+a33+a34+a35+a36+a37+a38+a39
    return kt


def get_corrected_kt(
        J: float,
        PD: float,
        AeAo: float,
        nblades: int,
        Re: float,
) -> float:
    kt = _get_kt(J=J, PD=PD, AeAo=AeAo, nblades=nblades)
    delta_kt = _get_delta_kt(J=J, PD=PD, AeAo=AeAo,
                             nblades=nblades, Re=Re)

    # Theoretically, we should add delta_kt only if Re > 2*(10**6)
    # However, it seems that the spreadsheet adds it regardless of the Re value
    return kt + delta_kt
