# External imports
from math import pi
import itertools
from typing import cast

# Internal imports
from shared_types import Input, Output
from reynolds_number import get_Re
from kt import get_corrected_kt
from kq import get_corrected_kq
from cavitation import get_cavitation_evaluation


def get_sorted_propulsion_systems(input: Input) -> Output:
    '''Function that returns a list of propulsion systems ordered by efficiency, within the imposed constraints.

    Parameters:
        input (Input): Dictionary containing the input parameters

    Returns:
        Output: List of propulsion systems ordered by efficiency
    '''

    # Constraints
    constraints = input['constraints']
    T_delivered_min = constraints['T_delivered_min']
    T_delivered_max = constraints['T_delivered_max']

    # Environment parameters
    environment = input['environment']
    rho = environment['rho']
    v = environment['v']
    g = environment['g']
    Pa = environment['Pa']
    Ps = environment['Ps']

    design_parameters = input['design_parameters']
    combinations = itertools.product(
        # All posible combinations of design parameters
        # TODO: somehow use something like itertools.product(*design_parameters.values()),
        # but in a clear and type safe way
        design_parameters['nblades_list'],
        design_parameters['rpms_list'],
        design_parameters['pds_list'],
        design_parameters['aeaos_list'],
        design_parameters['diameters_list'],
        design_parameters['w_list'],
        design_parameters['Vs_list'],
        design_parameters['T_list'],

    )

    unsorted_output: Output = []
    for nblades, RPM, PD, AeAo, d, w, Vs, T in combinations:
        # For some reason, mypy doesn't understand that nblades is an int
        nblades = cast(int, nblades)

        n = RPM/60  # rotation in Hz
        Va = Vs * (1-w)  # advance velocity
        J = Va / (n*d)  # advance ratio

        Re = get_Re(
            Va=Vs,  # Alho references as Va but uses Vs on spreadsheet as well
            n=n,
            d=d,
            v=v,
            nblades=nblades,
            AeAo=AeAo
        )

        kt = get_corrected_kt(J=J, PD=PD, AeAo=AeAo, nblades=nblades, Re=Re)
        T_delivered = (kt*rho*(n**2)*(d**4))/1000

        if T_delivered < T_delivered_min or T_delivered > T_delivered_max:
            continue

        shaft_depth = T - 0.55*d  # shaft depth
        cavitation_eval = get_cavitation_evaluation(
            rho=rho,
            Pa=Pa,
            Ps=Ps,
            g=g,
            T=T,
            d=d,
            T_delivered=T_delivered,
            shaft_depth=shaft_depth,
            Va=Vs,  # Alho references as Va but uses Vs on spreadsheet as well
            PD=PD,
            AeAo=AeAo,
            n=n,
            cavitation_limit=constraints['cavitation_limit']
        )

        if constraints['must_not_cavitate'] and cavitation_eval == 'nok':
            continue

        kq = get_corrected_kq(J=J, PD=PD, AeAo=AeAo,
                              nblades=nblades, Re=Re)

        efficiency = (J*kt)/(2*pi*kq)
        if efficiency < constraints['min_efficiency']:
            continue

        Q0 = kq*rho*(n**2)*(d**5) / 1000

        unsorted_output.append({
            'z': nblades,
            'N': RPM,
            'P/D': PD,
            'AeAo': AeAo,
            'd': d,
            'w': w,
            'Vs': Vs,
            'T': T,

            'J0': J,
            'Va': Va,

            'Kt0': kt,
            'T0': T_delivered,

            'Kq0': kq,
            'Q0': Q0,

            'efficiency': efficiency,
            'DHP': 2*pi*Q0*n,

            'cavitation_eval': cavitation_eval,
        })

    sorted_output = sorted(
        unsorted_output,
        key=lambda item: item['efficiency'],
        reverse=True
    )

    if constraints['max_number_of_outputed_systems'] == -1:
        # Get all systems
        return sorted_output

    return sorted_output[0:constraints['max_number_of_outputed_systems']]
