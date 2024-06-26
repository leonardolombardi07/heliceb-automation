# External imports
from typing import TypedDict, Literal, Sequence, Union, Any
import numpy as np


EnvironmentInput = TypedDict('EnvironmentInput', {
    'rho': float,  # kg/m^3, fluid density
    'v': float,  # m^2/s, fluid kinematic viscosity
    'g': float,  # m/s^2, acceleration of gravity
    'Pa': float,  # Pa, atmospheric pressure
    'Ps': float,  # Pa, saturation pressure of water
})

ConstraintsInput = TypedDict('ConstraintsInput', {
    # Number of propulsion systems to get. -1 means get all possible propulsion systems
    'max_number_of_outputed_systems': int,

    # Minimum efficiency. We won't consider propellers with efficiency below this value
    'min_efficiency': float,

    # If True, propellers that may cavitate will be excluded
    'must_not_cavitate': bool,

    # Minimum delivered thrust, in kN
    'T_delivered_min': float,

    # Maximum delivered thrust, in kN. float('inf') = infinity = means no limit
    'T_delivered_max': float,

    # Cavitation limit. Example: use 0.05 for 5% of cavitation limit
    'cavitation_limit': float,
})

IntListLike = Union[Sequence[int], np.ndarray[Any, Any]]
FloatListLike = Union[Sequence[float], np.ndarray[Any, Any]]

DesignParameters = TypedDict('DesignParameters', {
    # Sequence of number of blades to consider
    'nblades_list': IntListLike,

    # Sequence of rotations (in RPM) to consider, in rotations per minute
    'rpms_list': FloatListLike,

    # Sequence of pitch/diameter ratios to consider
    'pds_list': FloatListLike,

    # Sequence of area ratios to consider
    'aeaos_list': FloatListLike,

    # Sequence of propeller diameters to consider, in meters
    'diameters_list': FloatListLike,

    # Sequence of wake coefficients to consider
    'w_list': FloatListLike,

    # Sequence of ship speeds to consider, in m/s
    'Vs_list': FloatListLike,

    # Sequence of ship drafts to consider, in meters
    'T_list': FloatListLike,
})

Input = TypedDict('Input', {
    'environment': EnvironmentInput,
    'constraints': ConstraintsInput,
    'design_parameters': DesignParameters,
})

# To be consistent with Alho's spreadsheet
CavitationEvaluation = Literal['ok', 'nok']

OutputedPropulsionSystem = TypedDict('OutputedPropulsionSystem', {
    # Inputs on Alho's spreadsheet
    'z': int,  # number of blades
    'N': float,  # rpm, rotation
    'P/D': float,  # pitch/diameter ratio
    'AeAo': float,  # area ratio
    'd': float,  # m, propeller diameter
    'w': float,  # wake fraction
    'Vs': float,  # m/s, ship speed
    'T': float,  # m, ship draft

    # Outputs on Alho's spreadsheet
    'J0': float,  # advance ratio
    'Va': float,  # m/s, advance velocity

    'Kt0': float,  # thrust coefficient
    'T0': float,  # kN, propeller thrust

    'Kq0': float,  # torque coefficient
    'Q0': float,  # kN.m, propeller torque

    'efficiency': float,  # propeller efficiency
    'DHP': float,  # delivered horsepower

    'cavitation_eval': CavitationEvaluation,  # cavitation evaluation
})

Output = Sequence[OutputedPropulsionSystem]

Run = TypedDict('Run', {
    'input': Input,
    'output': Output,
})
