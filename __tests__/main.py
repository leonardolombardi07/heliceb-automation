# External imports
import sys
import xlwings as xw  # type: ignore
from typing import no_type_check, cast, List, Any
import os
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # nopep8

# Disable formatting for this line. We need to keep it before the internal imports
sys.path.append('.')  # nopep8

# Internal imports
from shared_types import EnvironmentInput, ShipInput, ConstraintsInput, Input, OutputedPropulsionSystem
from get_sorted_propulsion_systems import get_sorted_propulsion_systems


# Workbook related constants
ALHO_WORKBOOK = xw.Book(  # type: ignore
    f'{CURRENT_DIRECTORY}/PSM (EEN554) - HéliceB (Versão 2021).xlsm')
PRINCIPAL_SHEET = ALHO_WORKBOOK.sheets['Principal']  # type: ignore
ALHO_WORKBOOK_EXECUTAR_MACRO_NAME = 'Executar'


# General workbook constants
# We consider those to be equal to the values on the workbook

ENVIRONMENT_INPUT: EnvironmentInput = {
    'rho': 1025.9,  # densidade da água do mar, kg/m^3
    'v': 0.00000118831,  # viscosidade cinemática da água do mar, m^2/s
    'g': 9.807,  # aceleração da gravidade, m/s^2
    'Pa': 101_325,  # pressão atmosférica, Pa
    'Ps': 1705.1,  # pressão de saturação da água, Pa
}

SHIP_INPUT: ShipInput = {
    'd': 4,  # diâmetro do propulsor, m
    'w': 0.139,  # coeficiente de esteira
    'Vs': 6.945,  # velocidade de serviço do navio, m/s
    'T_required': 117.25,  # empuxo requerido, kN
    'T': 6,  # calado do navio na perpendicular de vante, m
}

CONSTRAINTS_INPUT: ConstraintsInput = {
    'max_number_of_outputed_systems': -1,
    'must_not_cavitate': False,  # se True, só retornará propulsores que não cavitem
    'min_efficiency': 0,  # eficiência mínima do propulsor
    'T_min_%': 0,  # 1 significa 100% do empuxo requerido
    # 10_000_000 significa 10_000_000% do empuxo requerido (um valor muito alto para não ser considerado)
    'T_max_%': 10_000_000,
    'cavitation_limit': 0.05,  # limite de cavitação
}

# Test related constants
MAX_RELATIVE_PERCENTUAL_DISCREPANCY = 0.01  # 0.01 = 1%, 0.1 = 10%, etc.


def _run_tests():
    print('Running tests...')
    print(f'''Max relative percentual discrepancy accepted: {
          MAX_RELATIVE_PERCENTUAL_DISCREPANCY*100}%''')
    print("\n")

    # Edit here the kind of prop systems you want to test
    prop_systems_to_test = [
        _create_prop_system_input(
            nblades=3, rpms=120, pds=0.95, aeaos=0.3
        ),
        _create_prop_system_input(
            nblades=4, rpms=150, pds=0.95, aeaos=0.3
        ),
        _create_prop_system_input(
            nblades=2, rpms=110, pds=0.8, aeaos=0.4
        ),
    ]

    for i, input in enumerate(prop_systems_to_test):
        print(f'Running test for prop {i+1} system...')
        _print_prop_system_input(input=input)
        _check_if_alho_spreadsheet_output_is_close_enough_to_software_output(
            input=input
        )
        print("\n")

    print('All tests passed!')


######### Helper functions #########


def _create_prop_system_input(nblades: int, rpms: int, pds: float, aeaos: float) -> Input:
    return {
        'environment': ENVIRONMENT_INPUT,
        'ship': SHIP_INPUT,
        'constraints': CONSTRAINTS_INPUT,
        'design_parameters': {
            'nblades_list': [nblades],
            'rpms_list': [rpms],
            'pds_list': [pds],
            'aeaos_list': [aeaos],
        }
    }


def _print_prop_system_input(input: Input):
    print(f'''Prop System Input:
          Number of Blades: {input['design_parameters']['nblades_list'][0]},
          RPM: {input['design_parameters']['rpms_list'][0]},
          P/D: {input['design_parameters']['pds_list'][0]},
          Ae/Ao: {input['design_parameters']['aeaos_list'][0]}
          ''')


@no_type_check
def _input_data_on_Alho_workbook(input: Input):
    # No type check because xlwings is not typed

    PRINCIPAL_SHEET.range(
        'F11').value = input['design_parameters']['nblades_list'][0]
    PRINCIPAL_SHEET.range('F12').value = input['ship']['d']
    PRINCIPAL_SHEET.range(
        'F13').value = input['design_parameters']['rpms_list'][0]
    PRINCIPAL_SHEET.range(
        'F14').value = input['design_parameters']['pds_list'][0]
    PRINCIPAL_SHEET.range(
        'F15').value = input['design_parameters']['aeaos_list'][0]

    PRINCIPAL_SHEET.range(
        'J11').value = input['ship']['Vs'] * 1.94384  # m/s to knots
    PRINCIPAL_SHEET.range('J14').value = input['ship']['T']
    PRINCIPAL_SHEET.range(
        'J17').value = input['constraints']['cavitation_limit']

    PRINCIPAL_SHEET.range('N11').value = input['ship']['w']


@no_type_check
def _get_outputed_system_from_Alho_workbook(input: Input) -> OutputedPropulsionSystem:
    # No type check because xlwings is not typed

    # Input data on workbook
    _input_data_on_Alho_workbook(input)

    # Execute macro
    ALHO_WORKBOOK.macro(ALHO_WORKBOOK_EXECUTAR_MACRO_NAME).run()

    # Get output data
    return {
        'z': PRINCIPAL_SHEET.range('F11').value,
        'N': PRINCIPAL_SHEET.range('F13').value,
        'P/D': PRINCIPAL_SHEET.range('F14').value,
        'AeAo': PRINCIPAL_SHEET.range('F15').value,

        'J0': PRINCIPAL_SHEET.range('K23').value,
        'Va': PRINCIPAL_SHEET.range('K24').value,

        'Kt0': PRINCIPAL_SHEET.range('K26').value,
        'T0': PRINCIPAL_SHEET.range('K27').value,

        'Kq0': PRINCIPAL_SHEET.range('K29').value,
        'Q0': PRINCIPAL_SHEET.range('K30').value,

        'efficiency': PRINCIPAL_SHEET.range('K32').value,
        'DHP': PRINCIPAL_SHEET.range('K33').value,

        'cavitation_eval': PRINCIPAL_SHEET.range('K35').value,
    }


def _assert_numbers_are_close_enough(key: str, wb_num: float, num: float, relative_percentual_discrep_tol: float):
    if wb_num == 0 and num == 0:
        return  # Both are 0, so they are close enough

    if wb_num == 0:
        # Use num as reference. Better than nothing...
        relative_percentual_discrepancy = abs(wb_num - num) / num

    else:
        relative_percentual_discrepancy = abs(
            wb_num - num) / wb_num

    assert relative_percentual_discrepancy <= relative_percentual_discrep_tol, f'''
    Error on key "{key}"
    Number on Spreadsheet: {wb_num},
    Number on Software: {num},
    Found Discrepancy: {round(relative_percentual_discrepancy, 2)*100}%,
    Max Discrepancy: {relative_percentual_discrep_tol*100}%
    '''


def _check_if_alho_spreadsheet_output_is_close_enough_to_software_output(input: Input):
    assert all([
        len(cast(List[Any], num)) == 1 for num in input['design_parameters'].values()
    ]), f'Test only works for an input of a single prop system. Input: {input}'

    software_output_prop_system = get_sorted_propulsion_systems(input=input)[
        0]
    alho_output_prop_system = _get_outputed_system_from_Alho_workbook(
        input=input)

    for key, val in software_output_prop_system.items():
        if key == 'cavitation_eval':
            alho_val = 'ok' if alho_output_prop_system[key] == 'ok' else 'not ok'
            assert software_output_prop_system[key] == alho_val, f'''
            Error on key "{key}"
            Value on Software: {software_output_prop_system[key]},
            Value on Spreadsheet: {alho_output_prop_system[key]}
            '''

        elif isinstance(val, int) or isinstance(val, float):
            wb_num = cast(float, alho_output_prop_system[key])
            _assert_numbers_are_close_enough(
                key=key,
                wb_num=wb_num,
                num=val,
                relative_percentual_discrep_tol=MAX_RELATIVE_PERCENTUAL_DISCREPANCY
            )

        else:
            print(f'Unknown key: {key}. Skipping test for this key.')


if __name__ == '__main__':
    _run_tests()
