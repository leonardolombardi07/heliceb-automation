# type: ignore
# TODO: add a stub file to xlwings

# External imports
import xlwings as xw
from shared_types import Run, Input, Output

# Internal imports
from datetime import datetime


def _write_input_sht(sht: xw.Sheet, input: Input):
    sht.range('A1').value = 'Environment'
    sht.range('A2').value = 'rho [kg/m³]'
    sht.range('B2').value = input['environment']['rho']

    sht.range('A4').value = 'Ship'
    sht.range('A5').value = 'd [m]'
    sht.range('B5').value = input['ship']['d']
    sht.range('A6').value = 'w [m]'
    sht.range('B6').value = input['ship']['w']
    sht.range('A7').value = 'Vs [m/s]'
    sht.range('B7').value = input['ship']['Vs']
    sht.range('A8').value = 'T_required [kN]'
    sht.range('B8').value = input['ship']['T_required']
    sht.range('A9').value = 'T [kN]'
    sht.range('B9').value = input['ship']['T']

    sht.range('A11').value = 'Constraints'
    sht.range('A12').value = 'max_number_of_outputed_systems'
    sht.range(
        'B12').value = input['constraints']['max_number_of_outputed_systems']
    sht.range('A13').value = 'must_not_cavitate'
    sht.range('B13').value = input['constraints']['must_not_cavitate']
    sht.range('A14').value = 'min_efficiency'
    sht.range('B14').value = input['constraints']['min_efficiency']
    sht.range('A15').value = 'T_min_%'
    sht.range('B15').value = input['constraints']['T_min_%']
    sht.range('A16').value = 'T_max_%'
    sht.range('B16').value = input['constraints']['T_max_%']

    sht.range('A18').value = 'Design Parameters'
    sht.range('A19').value = 'nblades_list'
    sht.range('B19').value = ', '.join(
        map(str, input['design_parameters']['nblades_list']))
    sht.range('A20').value = 'rpms_list'
    sht.range('B20').value = ', '.join(
        map(str, input['design_parameters']['rpms_list']))
    sht.range('A21').value = 'pds_list'
    sht.range('B21').value = ', '.join(
        map(str, input['design_parameters']['pds_list']))
    sht.range('A22').value = 'aeaos_list'
    sht.range('B22').value = ', '.join(
        map(str, input['design_parameters']['aeaos_list']))

    # Apply styles
    sht.range('A1:B22').api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
    sht.range('A1:B22').api.VerticalAlignment = xw.constants.VAlign.xlVAlignCenter
    sht.range('A1:B22').api.WrapText = True
    sht.range('A1:B22').column_width = 20

    # Give some border to the cells
    sht.range('A1:B22').api.Borders.LineStyle = 1
    sht.range('A1:B22').api.Borders.Weight = 2
    sht.range('A1:B22').api.Borders.Color = 0x000000


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
    sht.range('L1').value = 'Cavitação'

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
        sht.range(f'L{i+2}').value = propulsion_system['cavitation_eval']

    last_row = len(output) + 1

    all_range = f'A1:L{last_row}'
    headers_range = 'A1:L1'
    data_range = f'A2:L{last_row}'

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
