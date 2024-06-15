# type: ignore
# TODO: add a stub file to xlwings

# External imports
import xlwings as xw
from datetime import datetime
from typing import List

# Internal imports
from shared_types import Run, Input, Output


def _write_input_sht(sht: xw.Sheet, input: Input):
    sht.range('A1').value = 'Parâmetro'
    sht.range('B1').value = 'Valor'

    row = 2

    # Environment
    sht.range(f'A{row}').value = 'Environment'
    sht.range(f'A{row}:B{row}').merge()

    for key, value in input['environment'].items():
        row += 1
        sht.range(f'A{row}').value = key
        sht.range(f'B{row}').value = value

    # Constraints
    row += 1
    sht.range(f'A{row}').value = 'Constraints'
    sht.range(f'A{row}:B{row}').merge()

    for key, value in input['constraints'].items():
        row += 1
        sht.range(f'A{row}').value = key
        sht.range(f'B{row}').value = value

    # Design Parameters
    row += 1
    sht.range(f'A{row}').value = 'Design Parameters'
    sht.range(f'A{row}:B{row}').merge()

    def _list_as_str(lst: List[any]):
        return ', '.join(map(str, lst))

    for key, value in input['design_parameters'].items():
        row += 1
        sht.range(f'A{row}').value = key
        sht.range(f'B{row}').value = _list_as_str(value)

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
    sht.range('E1').value = 'Diâmetro (d) [m]'
    sht.range('F1').value = 'Coeficiente de Esteira (w)'
    sht.range('G1').value = 'Velocidade de Serviço (Vs) [m/s]'
    sht.range('H1').value = 'Calado (T) [m]'
    sht.range('I1').value = 'Coef. Avanço (J0)'
    sht.range('J1').value = 'Velocidade de Avanço (Va) [m/s]'
    sht.range('K1').value = 'Coeficiente de Empuxo (Kt0)'
    sht.range('L1').value = 'Empuxo (T0) [kN]'
    sht.range('M1').value = 'Coeficiente de Torque (Kq0)'
    sht.range('N1').value = 'Torque (Q0) [kN.m]'
    sht.range('O1').value = 'Eficiência (n0 x nrr)'
    sht.range('P1').value = 'Potência (DHP) [kW]'
    sht.range('Q1').value = 'Cavitação'

    for i, propulsion_system in enumerate(output):
        row = i + 2
        sht.range(f'A{row}').value = propulsion_system['z']
        sht.range(f'B{row}').value = propulsion_system['N']
        sht.range(f'C{row}').value = propulsion_system['P/D']
        sht.range(f'D{row}').value = propulsion_system['AeAo']
        sht.range(f'E{row}').value = propulsion_system['d']
        sht.range(f'F{row}').value = propulsion_system['w']
        sht.range(f'G{row}').value = propulsion_system['Vs']
        sht.range(f'H{row}').value = propulsion_system['T']
        sht.range(f'I{row}').value = propulsion_system['J0']
        sht.range(f'J{row}').value = propulsion_system['Va']
        sht.range(f'K{row}').value = propulsion_system['Kt0']
        sht.range(f'L{row}').value = propulsion_system['T0']
        sht.range(f'M{row}').value = propulsion_system['Kq0']
        sht.range(f'N{row}').value = propulsion_system['Q0']
        sht.range(f'O{row}').value = propulsion_system['efficiency']
        sht.range(f'P{row}').value = propulsion_system['DHP']
        sht.range(f'Q{row}').value = propulsion_system['cavitation_eval']

    last_column = 'Q'
    last_row = len(output) + 1

    all_range = f'A1:{last_column}{last_row}'
    headers_range = f'A1:{last_column}1'
    data_range = f'A2:{last_column}{last_row}'

    # Format of cells
    sht.range(data_range).number_format = '0.00'
    sht.range(f'A2:A{last_row}').number_format = '0'
    sht.range(f'K2:K{last_row}').number_format = '0.000'
    sht.range(f'M2:M{last_row}').number_format = '0.000'

    # Apply styles
    sht.tables.add(sht.used_range, table_style_name='TableStyleMedium1')
    sht.range(headers_range).column_width = 10
    sht.range(all_range).api.WrapText = True
    sht.range(
        all_range).api.HorizontalAlignment = xw.constants.HAlign.xlHAlignCenter
    sht.range(all_range).api.VerticalAlignment = xw.constants.VAlign.xlVAlignCenter


def save_as_excel(run: Run):
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
