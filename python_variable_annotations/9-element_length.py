#!/usr/bin/env python3
from typing import Iterable, Sequence, List, Tuple

def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns a list of tuples where each tuple contains an element from the input list
    and its corresponding length.

    Parameters:
      - lst (Iterable[Sequence]): The input list of sequences.

    Returns:
      - List[Tuple[Sequence, int]]: A list of tuples containing each element from the input
                                    list and its corresponding length.

    Example:
      >>> element_length(["apple", "banana", "orange"])
      [('apple', 5), ('banana', 6), ('orange', 6)]
    """
    return [(i, len(i)) for i in lst]
