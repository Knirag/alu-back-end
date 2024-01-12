#!/usr/bin/env python3
from typing import List, Union

def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Returns the sum of a list of integers and floats.

    Parameters:
      - mxd_lst (List[Union[int, float]]): The mixed list of integers and floats.

    Returns:
      - float: The sum of the mixed list.

    Example:
      >>> sum_mixed_list([5, 4, 3.14, 666, 0.99])
      679.13
    """
    return sum(mxd_lst)
