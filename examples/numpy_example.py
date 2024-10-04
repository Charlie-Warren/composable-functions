try:
    import numpy as np
except ImportError:
    print("numpy is not installed. Please install it before running this example.")
    exit()
import composablefunctions as cf

def multiply_by_two(arr: np.ndarray) -> np.ndarray:
    return arr * 2

def add_one(arr: np.ndarray) -> np.ndarray:
    return arr + 1

# ComposedFunction also works on numpy arrays.
# The key thing is that the type of the first argument must match the type of the return value.

composed = cf.ComposedFunction()

composed.add_function(multiply_by_two)
composed.add_function(add_one)

input_arr = np.array([1, 2, 3, 4, 5])
print(composed.apply(input_arr))