from shared_types import Output


def pretty_print(output: Output):
    for item in output:
        for key, value in item.items():
            if isinstance(value, float):
                print(f'{key}: {value:.2f}')
            else:
                print(f'{key}: {value}')
        print("\n")
