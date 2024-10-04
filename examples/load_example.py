import composablefunctions as cf
from pathlib import Path
from examples.my_float_lib_example import multiply_by_two, add_one_or_two, foo

SCRIPT_DIR = Path(__file__).parent.absolute()

def main():
    # Example of using the ComposedFunction class to load from a json
    composed = cf.ComposedFunction()

    # For loading you need to first let the ComposedFunction know what functions
    # are available sop they can be matched to the json
    available_funcs = [multiply_by_two, add_one_or_two, foo]
    composed.set_available_funcs(available_funcs)

    try:
        composed.load(SCRIPT_DIR / 'composed_function.json')
    except FileNotFoundError:
        print("Can't find json, skipping loading")

    composed.print_functions(show_args=True, show_kwargs=True)

    input_data = 3.5
    print(f"{input_data=}")
    result = composed.apply(input_data)
    print(f"{result=}")

if __name__ == "__main__":
    main()