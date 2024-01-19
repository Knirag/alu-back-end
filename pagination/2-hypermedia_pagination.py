#!/usr/bin/env python3
"""Hypermedia pagination."""
import csv
from math import ceil
from typing import List, Tuple, Dict


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

    def get_page(self, current_page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get the specified page.

        Args:
            current_page: Current page number.
            page_size: Total size of each page.

        Returns:
            List representing the specified page.
        """
        assert isinstance(current_page, int) and current_page > 0
        assert isinstance(page_size, int) and page_size > 0

        page_range: Tuple[int, int] = calculate_index_range(current_page, page_size)
        pagination: List = self.dataset()

        return pagination[page_range[0]:page_range[1]]

    def get_hyper(self, current_page: int = 1, page_size: int = 10) -> Dict:
        """
        Get hypermedia information for pagination.

        Args:
            current_page: Current page number.
            page_size: Total size of each page.

        Returns:
            Dictionary with pagination information.
        """
        data = []
        try:
            data = self.get_page(current_page, page_size)
        except AssertionError:
            return {}

        dataset: List = self.dataset()
        total_pages: int = ceil(len(dataset) / page_size) if dataset else 0
        previous_page: int = (current_page - 1) if (current_page - 1) >= 1 else None
        next_page: int = (current_page + 1) if (current_page + 1) <= total_pages else None

        hypermedia_info: Dict = {
            'page_size': page_size,
            'page': current_page,
            'data': data,
            'next_page': next_page,
            'prev_page': previous_page,
            'total_pages': total_pages,
        }

        return hypermedia_info


def calculate_index_range(current_page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate the range of items for the given page.

    Args:
        current_page: Current page number.
        page_size: Total size of each page.

    Returns:
        Tuple with the start and end indices of the page range.
    """
    final_index: int = current_page * page_size
    start_index: int = final_index - page_size

    return start_index, final_index
