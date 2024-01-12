#!/usr/bin/env python3
from typing import Union, Tuple

def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Returns a tuple with the first element as the string 'k'
    and the second element as the square of the int/float 'v'.

    Parameters:
      - k (str): The string key.
      - v (Union[int, float]): The value, which can be an int or a float.

    Returns:
      - Tuple[str, float]: A tuple containing 'k' and the square of 'v'.

    Example:
      >>> to_kv("eggs", 3)
      ('eggs', 9.0)
      >>> to_kv("school", 0.02)
      ('school', 0.0004)
    """
    return k, v ** 2.0
