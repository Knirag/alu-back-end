#!/usr/bin/env python3
from typing import List

def sum_list(input_list: List[float]) -> float:
    """
    Returns the sum of a list of floats.

    Parameters:
      - input_list (List[float]): The list of floats.

    Returns:
      - float: The sum of the input list.

    Example:
      >>> sum_list([3.14, 1.11, 2.22])
      6.47
    """
    return sum(input_list)
