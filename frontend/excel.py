# type: ignore
# TODO: add a stub file to xlwings

# External imports
import xlwings as xw
from shared_types import Run, Input, Output

# Internal imports
from datetime import datetime


def _write_input_sht(sht: xw.Sheet, input: Input):
    sht.range('A1').value = 'Parâmetro'
    sht.range('B1').value = 'Valor'

    row = 2

    # Environment
    sht.range(f'A{row}').value = 'Environment'
    sht.range(f'A{row}:B{row}').merge()

    row += 1
    sht.range(f'A{row}').value = 'rho [kg/m³]'
    sht.range(f'B{row}').value = input['environment']['rho']

    row += 1
    sht.range(f'A{row}').value = 'v [m²/s]'
    sht.range(f'B{row}').value = input['environment']['v']

    row += 1
    sht.range(f'A{row}').value = 'g [m/s²]'
    sht.range(f'B{row}').value = input['environment']['g']

    row += 1
    sht.range(f'A{row}').value = 'Pa [Pa]'
    sht.range(f'B{row}').value = input['environment']['Pa']

    row += 1
    sht.range(f'A{row}').value = 'Ps [Pa]'
    sht.range(f'B{row}').value = input['environment']['Ps']

    # Ship
    row += 1
    sht.range(f'A{row}').value = 'Ship'
    sht.range(f'A{row}:B{row}').merge()

    row += 1
    sht.range(f'A{row}').value = 'd [m]'
    sht.range(f'B{row}').value = input['ship']['d']

    row += 1
    sht.range(f'A{row}').value = 'w'
    sht.range(f'B{row}').value = input['ship']['w']

    row += 1
    sht.range(f'A{row}').value = 'Vs [m/s]'
    sht.range(f'B{row}').value = input['ship']['Vs']

    row += 1
    sht.range(f'A{row}').value = 'T_required [kN]'
    sht.range(f'B{row}').value = input['ship']['T_required']

    row += 1
    sht.range(f'A{row}').value = 'T [kN]'
    sht.range(f'B{row}').value = input['ship']['T']

    # Constraints
    row += 1
    sht.range(f'A{row}').value = 'Constraints'
    sht.range(f'A{row}:B{row}').merge()

    row += 1
    sht.range(f'A{row}').value = 'max_number_of_outputed_systems'
    sht.range(
        f'B{row}').value = input['constraints']['max_number_of_outputed_systems']

    row += 1
    sht.range(f'A{row}').value = 'must_not_cavitate'
    sht.range(f'B{row}').value = input['constraints']['must_not_cavitate']

    row += 1
    sht.range(f'A{row}').value = 'min_efficiency'
    sht.range(f'B{row}').value = input['constraints']['min_efficiency']

    row += 1
    sht.range(f'A{row}').value = 'T_min_%'
    sht.range(f'B{row}').value = input['constraints']['T_min_%']

    row += 1
    sht.range(f'A{row}').value = 'T_max_%'
    sht.range(f'B{row}').value = input['constraints']['T_max_%']

    row += 1
    sht.range(f'A{row}').value = 'cavitation_limit'
    sht.range(f'B{row}').value = input['constraints']['cavitation_limit']

    # Design Parameter
    row += 1
    sht.range(f'A{row}').value = 'Design Parameters'
    sht.range(f'A{row}:B{row}').merge()

    row += 1
    sht.range(f'A{row}').value = 'nblades_list'
    sht.range(f'B{row}').value = ', '.join(
        map(str, input['design_parameters']['nblades_list']))

    row += 1
    sht.range(f'A{row}').value = 'rpms_list'
    sht.range(f'B{row}').value = ', '.join(
        map(str, input['design_parameters']['rpms_list']))

    row += 1
    sht.range(f'A{row}').value = 'pds_list'
    sht.range(f'B{row}').value = ', '.join(
        map(str, input['design_parameters']['pds_list']))

    row += 1
    sht.range(f'A{row}').value = 'aeaos_list'
    sht.range(f'B{row}').value = ', '.join(
        map(str, input['design_parameters']['aeaos_list']))

    all_range = f'A1:B{row}'

    # Apply styles
    sht.range(all_range).api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
    sht.range(all_range).api.VerticalAlignment = xw.constants.VAlign.xlVAlignCenter
    sht.range(all_range).api.WrapText = True
    sht.range(all_range).column_width = 20

    # Give some border to the cells
    sht.range(all_range).api.Borders.LineStyle = 1
    sht.range(all_range).api.Borders.Weight = 2
    sht.range(all_range).api.Borders.Color = 0x000000


def _write_output_sht(sht: xw.Sheet, output: Output):
    sht.range('A1').value = 'Número de Pás (z)'
    sht.range('B1').value = 'Rotação (N) [rpm]'
    sht.range('C1').value = 'Razão de Passo (P/D)'
    sht.range('D1').value = 'Razão de Área (Ae/Ao)'
    sht.range('E1').value = 'Coef. Avanço (J0)'
    sht.range('F1').value = 'Velocidade de Avanço (Va) [m/s]'
    sht.range('G1').value = 'Coeficiente de Empuxo (Kt0)'
    sht.range('H1').value = 'Empuxo (T0) [kN]'
    sht.range('I1').value = 'Coeficiente de Torque (Kq0)'
    sht.range('J1').value = 'Torque (Q0) [kN.m]'
    sht.range('K1').value = 'Eficiência (n0 x nrr)'
    sht.range('L1').value = 'Potência (DHP) [kW]'
    sht.range('M1').value = 'Cavitação'

    for i, propulsion_system in enumerate(output):
        sht.range(f'A{i+2}').value = propulsion_system['z']
        sht.range(f'B{i+2}').value = propulsion_system['N']
        sht.range(f'C{i+2}').value = propulsion_system['P/D']
        sht.range(f'D{i+2}').value = propulsion_system['AeAo']
        sht.range(f'E{i+2}').value = propulsion_system['J0']
        sht.range(f'F{i+2}').value = propulsion_system['Va']
        sht.range(f'G{i+2}').value = propulsion_system['Kt0']
        sht.range(f'H{i+2}').value = propulsion_system['T0']
        sht.range(f'I{i+2}').value = propulsion_system['Kq0']
        sht.range(f'J{i+2}').value = propulsion_system['Q0']
        sht.range(f'K{i+2}').value = propulsion_system['efficiency']
        sht.range(f'L{i+2}').value = propulsion_system['DHP']
        sht.range(f'M{i+2}').value = propulsion_system['cavitation_eval']

    last_row = len(output) + 1

    all_range = f'A1:M{last_row}'
    headers_range = 'A1:M1'
    data_range = f'A2:M{last_row}'

    # Format of cells
    sht.range(data_range).number_format = '0.00'
    sht.range(f'A2:A{last_row}').number_format = '0'
    sht.range(f'E2:E{last_row}').number_format = '0.000'
    sht.range(f'F2:F{last_row}').number_format = '0.000'
    sht.range(f'G2:G{last_row}').number_format = '0.0000'
    sht.range(f'I2:I{last_row}').number_format = '0.0000'

    # Apply styles
    sht.tables.add(sht.used_range, table_style_name='TableStyleMedium1')
    sht.range(headers_range).column_width = 10
    sht.range(all_range).api.WrapText = True
    sht.range(
        all_range).api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
    sht.range(all_range).api.VerticalAlignment = xw.constants.VAlign.xlVAlignCenter


def save_to_excel(run: Run):
    wb = xw.Book()

    input_sht = wb.sheets[0]
    input_sht.name = 'Input'
    _write_input_sht(input_sht, run['input'])

    output_sht = wb.sheets.add()
    output_sht.name = 'Output'
    _write_output_sht(output_sht, run['output'])

    output_sht.activate()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(':', '-').replace(' ', '_')
    filename = f'run_{now}.xlsx'  # Example: "run_2024-05-10_21-02-54"
    wb.save(filename)
    print(f'Output on file "{filename}"')
