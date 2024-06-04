# External imports
import math
import numpy as np
from typing import Literal
import itertools

# Internal imports
from shared_types import Run, Input, Output
from kt import get_kt
from kq import get_kq
from cavitation import get_cavitation_evaluation
from frontend import pretty_print, save_to_excel


'''Leo: (10/05/2024)
Descrição do código:

Esse código varia parâmetros utilizados como input na planilha "Hélice B", do professor Alexandre Alho, pra encontrar os sistemas propulsivos com maior eficiência, dentro de certas restrições especificadas.

IMPORTANTE:
- (10/05/2024): a verificação da cavitação se restringe a um limite de cavitação de 5% (e não é confiável, já que se baseia em um código não verificado escrito por outras pessoas)

- (10/05/2024): os coeficientes de propulsão Kt e Kq calculados no código são ligeiramente diferentes dos da planilha do professor Alho, pois o código não inclui a contribuição de DeltaKT0 e DeltaKQ0 (considerados valores pequenos e que não afetam significativamente o resultado final)

- (06/04/2024): pra gerar um arquivo Excel com os resultados, é necessário ter a biblioteca xlwings instalada. Você pode instalar ela rodando o seguinte comando no seu terminal:
pip install xlwings

Para variar os parâmetros e restrições, altere as variáveis na seção "USER INPUTS" abaixo.

Pra entender melhor o que signfica cada valor de input, vá para o arquivo shared_types.py e veja a descrição de cada campo.
'''

########### USER INPUTS ###########

INPUT: Input = {
    # See shared_types.py for description of each field!

    'environment': {
        'rho': 1025.9
    },
    'ship': {
        'd': 3.5,
        'w': 0.277,
        'Vs': 6.94,
        'T_required': 43.15,  # 86.3/2
        'T': 6.3,
    },
    'constraints': {
        'max_number_of_best_propulsion_systems_to_get': -1,  # -1 to get all
        'must_not_cavitate': False,
        'min_efficiency': 0,
        'T_min_%': 0,
        'T_max_%': 10_000_000,  # 10_000_000 is analogous to infinity
    },
    'design_parameters': {
        'nblades_list': np.arange(start=3, stop=5 + 1, step=1),
        'rpms_list': np.arange(start=120, stop=200 + 10, step=10),
        'pds_list': np.arange(start=0.5, stop=1.4 + 0.05, step=0.05),
        'aeaos_list': np.arange(start=0.5, stop=1.4 + 0.05, step=0.05),
    }
}

'''Output type. Choose one of the following:
Print -> print results to the console
Excel -> save results to an excel file
'''
OUTPUT_TYPE: Literal["print", "excel"] = "excel"

########### END OF USER INPUTS ###########


def get_best_propulsion_systems(input: Input) -> Output:
    # Input Constants
    environment = input['environment']
    rho = environment['rho']

    # Input Ship parameters
    ship = input['ship']
    d = ship['d']
    Vs = ship['Vs']
    rho = input['environment']['rho']
    T_required = ship['T_required']
    w = ship['w']
    T = ship['T']

    # Calculated parameters
    Va = Vs * (1-w)  # advance velocity

    design_parameters = input['design_parameters']
    constraints = input['constraints']

    unsorted_output: Output = []

    # All posible combinations of design parameters
    combinations = itertools.product(
        # All posible combinations of design parameters
        design_parameters['nblades_list'],
        design_parameters['rpms_list'],
        design_parameters['pds_list'],
        design_parameters['aeaos_list']
    )
    for nblades, RPM, PD, AeAo in combinations:
        n = RPM/60  # rotation in Hz
        J = Va / (n*d)  # advance ratio

        kt = get_kt(J=J, PD=PD, AeAo=AeAo, nblades=nblades)
        T_delivered = (kt*rho*(n**2)*(d**4))/1000

        T_min = T_required * constraints['T_min_%']
        T_max = T_required * constraints['T_max_%']
        if T_delivered < T_min or T_delivered > T_max:
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

        if constraints['must_not_cavitate'] and cavitation_eval == "not ok":
            continue

        kq = get_kq(J=J, PD=PD, AeAo=AeAo,
                    nblades=nblades)

        efficiency = (J*kt)/(2*math.pi*kq)
        if efficiency < constraints['min_efficiency']:
            continue

        unsorted_output.append({
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
            'cavitation_eval': cavitation_eval,
        })

    return sorted(
        unsorted_output,
        key=lambda item: item['efficiency'],
        reverse=True
    )[: constraints['max_number_of_best_propulsion_systems_to_get']]


output = get_best_propulsion_systems(input=INPUT)

run: Run = {
    'input': INPUT,
    'output': output
}

if OUTPUT_TYPE == "print":  # type: ignore
    pretty_print(run)
elif OUTPUT_TYPE == "excel":  # type: ignore
    save_to_excel(run)
else:
    raise ValueError(f"Invalid OUTPUT_TYPE: {OUTPUT_TYPE}")
