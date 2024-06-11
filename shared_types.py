# External imports
from typing import TypedDict, Literal, Sequence, Union, Any
import numpy as np


EnvironmentInput = TypedDict('EnvironmentInput', {
    'rho': float,  # kg/m^3, fluid density
})

ShipInput = TypedDict('ShipInput', {
    'd': float,  # m, propeller diameter
    'w': float,  # coeficiente de esteira (TODO: write name in english)
    'Vs': float,  # m/s, ship speed
    'T_required': float,  # kN, required propeller thrust
    'T': float,  # m, ship draft
})

ConstraintsInput = TypedDict('ConstraintsInput', {
    # Number of propulsion systems to get. -1 means get all possible propulsion systems
    'max_number_of_outputed_systems': int,

    # Minimum efficiency. We won't consider propellers with efficiency below this value
    'min_efficiency': float,

    # If True, propellers that may cavitate will be excluded
    'must_not_cavitate': bool,

    # Minimum thrust, as percentage, compared with required. We won't consider propellers with thrust below this value
    'T_min_%': float,

    # Maximum thrust, as percentage, compared with required. We won't consider propellers with thrust above this value
    'T_max_%': float,
})

ListLike = Union[Sequence[int], np.ndarray[Any, Any]]

DesignParameters = TypedDict('DesignParameters', {
    # Sequence of number of blades to consider
    'nblades_list': ListLike,

    # Sequence of rotations (in RPM) to consider
    'rpms_list': ListLike,

    # Sequence of pitch/diameter ratios to consider
    'pds_list': ListLike,

    # Sequence of area ratios to consider
    'aeaos_list': ListLike,
})

Input = TypedDict('Input', {
    'environment': EnvironmentInput,
    'ship': ShipInput,
    'constraints': ConstraintsInput,
    'design_parameters': DesignParameters,
})

OutputedPropulsionSystem = TypedDict('OutputedPropulsionSystem', {
    # Inputs on Alho's spreadsheet
    'z': int,  # number of blades
    'N': int,  # rpm, rotation
    'P/D': float,  # pitch/diameter ratio
    'AeAo': float,  # area ratio

    # Outputs on Alho's spreadsheet
    'J0': float,  # advance ratio,
    'Va': float,  # m/s, advance velocity

    'Kt0': float,  # thrust coefficient
    'T0': float,  # kN, propeller thrust

    'Kq0': float,  # torque coefficient
    'Q0': float,  # kN.m, propeller torque

    'efficiency': float,  # propeller efficiency
    'cavitation_eval': Literal['ok', 'not ok'],
})

Output = Sequence[OutputedPropulsionSystem]

Run = TypedDict('Run', {
    'input': Input,
    'output': Output,
})
