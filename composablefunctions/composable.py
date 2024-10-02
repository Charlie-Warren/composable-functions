import json
from dataclasses import dataclass
from typing import Callable, Any, Union

import numpy as np

ComposableFunction = Callable[[np.ndarray, Any], np.ndarray]


@dataclass
class Composable:
    func: ComposableFunction
    args: tuple
    kwargs: dict
    enabled: bool


class ComposedFunction:
    def __init__(self):
        self.composables: list[Composable] = []
        self.available_funcs: list[ComposableFunction] = []

    def add_function(self, func: ComposableFunction, *args: Any, **kwargs: Any):
        """
        Add a custom function and its associated arguments.
        
        The first argument of your function should always be the input numpy array to apply
        the function to. Other arguments and keyword arguments can be passed to the function
        after the input array. Your function should return a numpy array.

        Example
        -------
        def foo(arr: np.ndarray, a: int, b: float) -> np.ndarray:
            return arr * a + b

        my_data = np.array([1, 2, 3])

        composed = ComposedFunction()

        composed.add_function(foo, a=2, b=3.5)

        composed.add_function(foo, a=5, b=8.1)
        
        composed.apply(my_data)
        """
        self.composables.append(
            Composable(func=func, args=args, kwargs=kwargs, enabled=True)
        )

    def remove_function(self, index: int):
        """Remove a function at the given index."""
        self.composables.pop(index)

    def set_new_index(self, index: int, new_index: int):
        """Moves the position of the function at the given index."""
        if index == new_index:
            return
        comp = self.composables.pop(index)
        self.composables.insert(new_index, comp)

    def clear_functions(self):
        """Remove all functions."""
        self.composables.clear()

    def move_up(self, index: int):
        """Move the function at the given index up one position."""
        if index > 0:
            self.set_new_index(index, index - 1)

    def move_down(self, index: int):
        """Move the function at the given index down one position."""
        if index < len(self.composables) - 1:
            self.set_new_index(index, index + 1)

    def get_enabled_state(self, index: int) -> bool:
        """Get the enabled state of the function at the given index. True if enabled, False if disabled."""
        return self.composables[index].enabled

    def set_enabled_state(self, index: int, enabled: bool):
        """Set the enabled/disabled state of the function at the given index."""
        self.composables[index].enabled = enabled

    def get_function_str(self, index: int, show_args: bool = False, show_kwargs: bool = False) -> str:
        """Get the string representation of the function at the given index."""
        comp = self.composables[index]
        func, args, kwargs, enabled = comp.func, comp.args, comp.kwargs, comp.enabled
        arg_str = ", ".join([str(arg) for arg in args])
        kwarg_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        arg_kwarg_str = ""
        if not show_args:
            arg_str = ""
        if not show_kwargs:
            kwarg_str = ""
        if arg_str and kwarg_str:
            arg_kwarg_str = f"{arg_str}, {kwarg_str}"
        elif arg_str:
            arg_kwarg_str = arg_str
        elif kwarg_str:
            arg_kwarg_str = kwarg_str
        return f"{func.__name__}({arg_kwarg_str}) enabled={enabled}"

    def print_functions(self, show_args: bool = False, show_kwargs: bool = False):
        for i in range(len(self.composables)):
            print(f"{i}: {self.get_function_str(i, show_args=show_args, show_kwargs=show_kwargs)}")

    def apply(self, arr: np.ndarray) -> np.ndarray:
        """Apply all functions in sequence to the array."""
        result = arr
        for composable in self.composables:
            func = composable.func
            args = composable.args
            kwargs = composable.kwargs
            if composable.enabled:
                result = func(result, *args, **kwargs)
        return result

    def save(self, filename: str):
        data = []
        for comp in self.composables:
            func = comp.func
            args = comp.args
            kwargs = comp.kwargs
            enabled = comp.enabled
            comp_dict = {
                'func': func.__name__,
                'args': args,
                'kwargs': kwargs,
                'enabled': enabled
            }
            data.append(comp_dict)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def _match_func(self, func_name: str) -> Union[ComposableFunction, None]:
        """Return the function from the list of available functions that matches the given name.
        If no function matches, return None."""
        available_func_names = [f.__name__ for f in self.available_funcs]
        if func_name not in available_func_names:
            return None
        return [func for func in self.available_funcs if func.__name__ == func_name][0]

    def load(self, filename: str):
        if not self.available_funcs:
            raise ValueError("No available functions to load. First use set_available_funcs to add valid functions.")

        with open(filename, 'r') as f:
            data = json.load(f)

        # check all functions are in the available functions
        for comp_dict in data:
            func_name = comp_dict['func']
            func = self._match_func(func_name)
            if func is None:
                raise ValueError(f"Function {func_name} not found in available functions")

        # if we get to this stage all functions are valid, so clear the current functions
        self.clear_functions()

        # match the function names with the available functions
        for comp_dict in data:
            func_name = comp_dict['func']
            func = self._match_func(func_name)
            args = comp_dict['args']
            kwargs = comp_dict['kwargs']
            enabled = comp_dict['enabled']
            self.add_function(func, *args, **kwargs)
            self.set_enabled_state(len(self) - 1, enabled)

    def get_available_funcs(self) -> list[ComposableFunction]:
        return self.available_funcs

    def set_available_funcs(self, available_funcs: list[ComposableFunction]):
        self.available_funcs = available_funcs

    def __str__(self) -> str:
        names = ", ".join([func[0].__name__ for func in self.composables])
        return f"ComposedFunction({names})"

    def __len__(self) -> int:
        return len(self.composables)
