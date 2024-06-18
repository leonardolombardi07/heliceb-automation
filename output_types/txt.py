# External imports
from datetime import datetime

# Internal imports
from shared_types import Run


def save_as_txt(run: Run):
    input = run['input']
    output = run['output']

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S').replace(':', '-').replace(' ', '_')
    filename = f'output_{now}.txt'  # Example: "output_2024-05-10_21-02-54"
    with open(filename, 'w') as f:
        f.write("Inputs\n\n")

        f.write("Environment\n")
        for key, value in input['environment'].items():
            f.write(f'{key}: {value}\n')

        f.write("\nConstraints\n")
        for key, value in input['constraints'].items():
            f.write(f'{key}: {value}\n')

        f.write("\nDesign Parameters\n")
        for key, value in input['design_parameters'].items():
            f.write(f'{key}: {value}\n')

        f.write("\nOutputs\n")

        # Write header
        for key in output[0].keys():
            f.write(f'{key} ')
        f.write('\n')

        # Write data
        for item in output:
            for value in item.values():
                f.write(f'{value} ')
            f.write('\n')
