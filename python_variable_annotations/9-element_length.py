#!/usr/bin/env python3
from typing import Callable

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Returns a function that multiplies a float by the given multiplier.

    Parameters:
      - multiplier (float): The multiplier to be used in the returned function.

    Returns:
      - Callable[[float], float]: A function that takes a float argument and
                                  returns the product of the argument and the multiplier.

    Example:
      >>> fun = make_multiplier(2.22)
      >>> fun(2.22)
      4.9284
    """
    def multiplier_function(x: float) -> float:
        return x * multiplier

    return multiplier_function
