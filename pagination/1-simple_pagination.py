#!/usr/bin/env python3
"""Simple pagination."""
import csv
from typing import List, Tuple


class BabyNameServer:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get the specified page.

        Args:
            page: Current page number.
            page_size: Total size of each page.

        Returns:
            List representing the specified page.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        page_range: Tuple[int, int] = calculate_page_range(page, page_size)
        pagination: List = self.dataset()

        return pagination[page_range[0]:page_range[1]]


def calculate_page_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the range of items for the given page.

    Args:
        page: Current page number.
        page_size: Total size of each page.

    Returns:
        Tuple with the start and end indices of the page range.
    """
    final_index: int = page * page_size
    start_index: int = final_index - page_size

    return start_index, final_index
