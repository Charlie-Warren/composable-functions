import composablefunctions as cf
from pathlib import Path
from examples.my_float_lib_example import multiply_by_two, add_one_or_two, foo

SCRIPT_DIR = Path(__file__).parent.absolute()

def main():
    # Example of using the ComposedFunction class to add functions and save to a json
    input_data = 3.5

    composed = cf.ComposedFunction()
    composed.add_function(multiply_by_two) # functions with only the np.ndarray argument are supported
    composed.add_function(add_one_or_two, False) # functions with extra args are supported
    composed.add_function(add_one_or_two, add_one=True) # functions with extra kwargs are supported
    composed.add_function(foo, 2, b=3, c=4.0, d=5.0) # functions with a mix of args and kwargs are supported

    composed.print_functions(True, True)
    result = composed.apply(input_data)
    print(f"{result=}\n")

    composed.set_enabled_state(index=2, enabled=False) # you can disable functions so they don't get applied

    composed.print_functions(True, True)
    result = composed.apply(input_data)
    print(f"{result=}\n")

    composed.save(SCRIPT_DIR / 'composed_function.json') # save the composed function to a json

if __name__ == "__main__":
    main()