#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


class BabyNameServer:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {i: dataset[i] for i in range(len(dataset))}
        return self.__indexed_dataset

def get_hyper_index(self, current_index: int = None, page_size: int = 10) -> Dict:
    """
    Get the hyper index.

    Args:
        current_index: Current index.
        page_size: Total size of the page.

    Return:
        Hyper index.
    """
    result_dataset = []
    index_data = self.indexed_dataset()
    keys_list = list(index_data.keys())
    assert current_index + page_size < len(keys_list)
    assert current_index < len(keys_list)

    if current_index not in index_data:
        start_index = keys_list[current_index]
    else:
        start_index = current_index

    for i in range(start_index, start_index + page_size):
        if i not in index_data:
            result_dataset.append(index_data[keys_list[i]])
        else:
            result_dataset.append(index_data[i])

    next_index: int = current_index + page_size

    if current_index in keys_list:
        next_index
    else:
        next_index = keys_list[next_index]

    return {
        'index': current_index,
        'next_index': next_index,
        'page_size': len(result_dataset),
        'data': result_dataset
    }
