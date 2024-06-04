from typing import TypedDict, Literal, Sequence


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
    'DHP': float,  # kW, propeller power
    'cavitation_eval': Literal['ok', 'not ok'],
})

Output = Sequence[OutputedPropulsionSystem]
