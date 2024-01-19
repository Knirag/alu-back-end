#!/usr/bin/env python3
"""Range simple helper function."""
from typing import Tuple


def calculate_page_range(current_page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the range of items for the given page.

    Args:
        current_page: Current page number.
        page_size: Total size of each page.

    Returns:
        Tuple with the start and end indices of the page range.
    """

    end_index: int = current_page * page_size
    start_index: int = end_index - page_size

    return (start_index, end_index)