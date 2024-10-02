import numpy as np
from composable import ComposedFunction
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()


def multiply_by_two(arr: np.ndarray) -> np.ndarray:
    return arr * 2


def add_one_or_two(arr: np.ndarray, add_one: bool) -> np.ndarray:
    if add_one:
        return arr + 1
    else:
        return arr + 2


def add_one(arr: np.ndarray) -> np.ndarray:
    return arr + 1


def foo(arr: np.ndarray, a: int, b: int, c: float, d: float) -> np.ndarray:
    return arr * a * b + c + d


def main():
    # Example of using the ComposedFunction class
    available_funcs = [multiply_by_two, add_one_or_two, add_one, foo]

    composed = ComposedFunction()
    composed.set_available_funcs(available_funcs)
    try:
        composed.load(SCRIPT_DIR / 'composed_function.json')
    except FileNotFoundError:
        print("Can't find json, skipping loading")

    composed.print_functions(True, True)

    input_data = np.array([1, 2, 3])
    print(f"{input_data=}")
    result = composed.apply(input_data)
    print(f"{result=}")


if __name__ == "__main__":
    main()
