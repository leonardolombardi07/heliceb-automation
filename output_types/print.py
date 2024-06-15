# Internal imports
from shared_types import Run


def pretty_print(run: Run):
    input = run['input']
    output = run['output']

    print("Inputs")
    print("\n")

    print("Environment")
    for key, value in input['environment'].items():
        print(f'{key}: {value}')

    print("\nConstraints")
    for key, value in input['constraints'].items():
        print(f'{key}: {value}')

    print("\nDesign Parameters")
    for key, value in input['design_parameters'].items():
        print(f'{key}: {value}')

    print("\nOutputs")
    for item in output:
        for key, value in item.items():
            if isinstance(value, float):
                print(f'{key}: {value:.2f}')
            else:
                print(f'{key}: {value}')
        print("\n")
