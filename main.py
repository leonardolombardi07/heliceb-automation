# External imports
from typing import Union, Literal

# Internal imports
from shared_types import Run, Input
from frontend import pretty_print, save_to_excel
from utils import np_arange_including_stop
from get_sorted_propulsion_systems import get_sorted_propulsion_systems


'''Leo: (12/06/2024)
Descrição do código:

Esse código automatiza o processo de variação de parâmetros de input utilizados na planilha "Hélice B" do professor Alexandre Alho.
Editando-se os parâmetros de input na seção 'INPUTS DO USUÁRIO' e executando o código, o programa gera uma lista de propulsores
(com suas características como empuxo entregado, kt, kq, etc...), ordenados por eficiência, dentro das restrições impostas.
O output pode ser mostrado no terminal/console (famoso "print") ou salvo em um arquivo Excel (necessário ter a biblioteca xlwings
instalada).

IMPORTANTE:
- (06/04/2024): pra gerar um arquivo Excel com os resultados, é necessário ter a biblioteca xlwings instalada.
Você pode instalar ela rodando o seguinte comando no seu terminal:
pip install xlwings
'''


########### INPUTS DO USUÁRIO ###########

'''Tipo de output. Selecionar entre:
Print | "print" -> printa os resultados no console
Excel | "excel" -> salva os resultados em um arquivo Excel (nomeado como "run_....xlsx")
None -> não faz nada. Útil para testar o código sem printar ou salvar os resultados'''
OUTPUT_TYPE: Union[
    Literal['print', 'excel'],
    None
] = "excel"  # <- Alterar aqui


INPUT: Input = {
    'environment': {
        'rho': 1025.9,  # densidade da água do mar, kg/m^3
        'v': 0.00000118831,  # viscosidade cinemática da água do mar, m^2/s
        'g': 9.807,  # aceleração da gravidade, m/s^2
        'Pa': 101_325,  # pressão atmosférica, Pa
        'Ps': 1705.1,  # pressão de saturação da água, Pa
    },
    'constraints': {
        # -1 significa que todos os sistemas serão retornados
        'max_number_of_outputed_systems': -1,
        'must_not_cavitate': False,  # se True, só retornará propulsores que não cavitem
        'min_efficiency': 0,  # eficiência mínima do propulsor
        'T_delivered_min': 43.15,  # Mínimo empuxo requerido
        'T_delivered_max': 10_000_000,  # Máximo empuxo requerido
        'cavitation_limit': 0.05,  # limite de cavitação
    },
    'design_parameters': {
        # Você pode usar listas normais aqui, tipo [3, 4, 5], mas np_arange_including_stop é mais prático

        # lista de número de pás, em RPM (exemplo: [3, 4, 5])
        'nblades_list': np_arange_including_stop(start=3, stop=5, step=1),
        # lista de rotações (RPM) (exemplo: [120, 130, 140, ..., 200])
        'rpms_list': np_arange_including_stop(start=120, stop=200, step=20),
        # lista de razões P/D (exemplo: [0.5, 0.55, 0.6, ..., 1.5])
        'pds_list': np_arange_including_stop(start=0.5, stop=1.5, step=0.5),
        # lista de razões de área Ae/Ao (exemplo: [0.3, 0.35, 0.4, ..., 1.1])
        'aeaos_list': np_arange_including_stop(start=0.5, stop=1.5, step=0.5),
        # lista de diâmetros, em m (exemplo: [3.5, 4, 4.5, ..., 6])
        'diameters_list': [3.5],
        # lista de coeficientes de esteira (exemplo: [0.25, 0.3, 0.35, ..., 0.6])
        'w_list': [0.277],
        # lista de velocidades do navio, em m/s (exemplo: [5.5, 6, 6.5, ..., 8])
        'Vs_list': [5.66],
        # lista de calados do navio na perpendicular de vante, em m (exemplo: [5, 5.5, 6, ..., 7.5])
        'T_list': [6.3],
    }
}


if __name__ == '__main__':
    output = get_sorted_propulsion_systems(input=INPUT)

    run: Run = {
        'input': INPUT,
        'output': output
    }

    if OUTPUT_TYPE == 'print':  # type: ignore
        pretty_print(run)
    elif OUTPUT_TYPE == 'excel':  # type: ignore
        save_to_excel(run)
    elif OUTPUT_TYPE is None:  # type: ignore
        pass
    else:
        raise ValueError(f'Invalid OUTPUT_TYPE: {OUTPUT_TYPE}')
