#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
            Get the hyper index

            Args:
                index: Current page
                page_size: Total size of the page

            Return:
                Hyper index
        """
        result_dataset = []
        # get the index data
        indexed_data = self.indexed_dataset()
        # extract all the index from the index dictionary
        keys_list = list(indexed_data.keys())
        # ensure index is within range in the index_data
        assert index + page_size <= len(keys_list)
        assert index < len(keys_list)

        if index not in indexed_data:
            start_index = keys_list[index]
        else:
            start_index = index

        for i in range(start_index, start_index + page_size):
            if i not in indexed_data:
                result_dataset.append(indexed_data[keys_list[i]])
            else:
                result_dataset.append(indexed_data[i])

        next_index: int = index + page_size

        if index not in keys_list:
            next_index = keys_list[next_index]

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(result_dataset),
            'data': result_dataset
        }
