# Functions can accept any type as the first argument,
# as long as it matches the type of the return value.
# They can have additional arguments and keyword arguments.
# They should return a type that matches the first argument.

def make_uppercase(mystring: str) -> str:
    return mystring.upper()

def foo(mystring: str, *args, **kwargs) -> str:
    ret = "I used foo with the primary argument: " + mystring + "."
    if args:
        ret += " It has additional argument(s): " + ", ".join([str(arg) for arg in args]) + "."
    if kwargs:
        ret += " It has additional keyword argument(s): " + ", ".join([f"{k}={v}" for k, v in kwargs.items()]) + "."
    return ret