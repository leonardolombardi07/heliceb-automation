import math
import numpy as np
from typing import TypedDict, Literal
from shared_types import Output
from kt import get_kt
from kq import get_kq
from cavitation import get_cavitation_evaluation
from frontend import pretty_print, save_to_excel

'''Leo: (10/05/2024)
Descrição do código:

Esse código varia parâmetros utilizados como input na planilha "Hélice B", do professor Alexandre Alho, pra encontrar os sistemas propulsivos com maior eficiência, dentro de certas restrições especificadas.

IMPORTANTE: 
- (10/05/2024): a verificação da cavitação se restringe a um limite de cavitação de 5% (e não é confiável, já que se baseia em um código não verificado e escrito por outras pessoas

- (10/05/2024): os coeficientes de propulsão Kt e Kq calculados no código são ligeiramente diferentes dos da planilha do professor Alho, pois o código não inclui a contribuição de DeltaKT0 e DeltaKQ0 (são valores pequenos e não afetam significativamente o resultado final)

Para variar os parâmetros e restrições, altere as variáveis antes da função get_best_propulsion_systems().
'''

'''Output type. Choose one of the following:
Print -> print results to the console
Excel -> save results to an excel file
'''
OUTPUT_TYPE: Literal["print", "excel"] = "excel"

Input = TypedDict('Input', {
    'd': float,  # m, propeller diameter
    'w': float,  # coeficiente de esteira (TODO: write name in english)
    'Vs': float,  # m/s, ship speed
    'rho': float,  # kg/m^3, fluid density
    'T_required': float,  # kN, required propeller thrust
    'Cp': float,  # ship prismatic coefficient
    'LCB': float,  # m, longitudinal center of buoyancy
    'T': float,  # m, ship draft
})


INPUT: Input = {
    'd': 3.5,  # m
    'Vs': 6.94,  # m/s
    'rho': 1025.9,  # kg/m^3
    'T_required': 86.3/2,  # kN
    'Cp': 0.6754,
    'LCB': 37.398,  # m,
    'T': 6.3,  # m
    'w': 0.277,
}


'''Number of best propulsion systems to get. We will get the best N systems, based on efficiency'''
NUMBER_OF_BEST_PROPULSION_SYSTEMS_TO_GET = 200

'''Minimum efficiency. We won't consider propellers with efficiency below this value'''
EFFICIENCY_MIN = 0.2

'''Minimum thrust, compared with required. We won't consider propellers with thrust below this value'''
T_MIN = 1

'''Maximum thrust, compared with required. We won't consider propellers with thrust above this value'''
T_MAX = 1.5

'''Sequence of number of blades to consider'''
NBLADES_LIST = np.arange(start=3, stop=5, step=1)  # type: ignore

'''Sequence of rotations (in RPM) to consider'''
RPMS = np.arange(start=120, stop=200, step=10)  # type: ignore

'''Sequence of pitch/diameter ratios to consider'''
PDS = np.arange(start=0.5, stop=1.4, step=0.05)  # type: ignore

'''Sequence of area ratios to consider'''
AEAOS = np.arange(start=0.5, stop=1.4, step=0.05)  # type: ignore


def get_best_propulsion_systems() -> Output:
    d = INPUT['d']
    Vs = INPUT['Vs']
    rho = INPUT['rho']
    T_required = INPUT['T_required']
    Cp = INPUT['Cp']
    LCB = INPUT['LCB']
    w = INPUT['w']
    T = INPUT['T']

    Va = Vs * (1-w)  # advance velocity
    THP = 2*T_required*Va  # total horse power

    output: Output = []
    for nblades in NBLADES_LIST:
        for RPM in RPMS:
            n = RPM/60  # rotation in Hz
            J = Va / ((RPM/60)*d)  # advance ratio

            for PD in PDS:
                nRR = 0.9737 + 0.111 * \
                    (Cp - 0.0225*LCB) - 0.06325*PD  # TODO: what is nRR?

                for AeAo in AEAOS:
                    kt = get_kt(J=J, PD=PD, AeAo=AeAo, nblades=nblades)

                    T_delivered = (kt*rho*(n**2)*(d**4))/1000
                    if T_delivered < T_MIN*T_required or T_delivered > T_MAX*T_required:
                        continue

                    cavitation_eval = get_cavitation_evaluation(
                        T=T,
                        T_delivered=T_delivered,
                        n=n,
                        d=d,
                        AeAo=AeAo,
                        PD=PD,
                        Va=Va,
                        rho=rho
                    )
                    # if cavitation_eval == "not ok":
                    #     continue

                    kq = get_kq(J=J, PD=PD, AeAo=AeAo,
                                nblades=nblades)

                    efficiency = (J*kt)/(2*math.pi*kq)
                    if efficiency < EFFICIENCY_MIN:
                        continue

                    output.append({
                        'z': nblades,
                        'N': RPM,
                        'P/D': PD,
                        'AeAo': AeAo,

                        'J0': J,
                        'Va': Va,

                        'Kt0': kt,
                        'T0': T_delivered,

                        'Kq0': kq,
                        'Q0': kq*rho*(n**2)*(d**5) / 1000,

                        'efficiency': efficiency,
                        'DHP': THP/(nRR*efficiency),

                        'cavitation_eval': cavitation_eval,
                    })

    return sorted(
        output,
        key=lambda PD: PD['efficiency'],
        reverse=True
    )[: NUMBER_OF_BEST_PROPULSION_SYSTEMS_TO_GET]


output = get_best_propulsion_systems()

if OUTPUT_TYPE == "print":  # type: ignore
    pretty_print(output)
elif OUTPUT_TYPE == "excel":  # type: ignore
    save_to_excel(output)
else:
    raise ValueError(f"Invalid OUTPUT_TYPE: {OUTPUT_TYPE}")
