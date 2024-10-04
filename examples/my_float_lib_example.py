# Functions can accept any type as the first argument,
# as long as it matches the type of the return value.
# They can have additional arguments and keyword arguments.
# They should return a type that matches the first argument.

def multiply_by_two(myfloat: float) -> float:
    return myfloat * 2

def add_one_or_two(myfloat: float, add_one: bool) -> float:
    if add_one:
        return myfloat + 1
    else:
        return myfloat + 2

def foo(myfloat: float, a: int, b: int, c: float, d: float) -> float:
    return myfloat * a * b + c + d