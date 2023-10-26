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
        data = []
        assert isinstance(page_size, int) and page_size > 0
        assert isinstance(index, int) or index is None
        assert 0 <= index < len(self.dataset())

        if index is None:
            index = 0
        nxt_idx = index
        indexed_dataset = self.indexed_dataset()

        while page_size > 0:
            data_content = indexed_dataset.get(nxt_idx)
            if data_content is not None:
                data.append(data_content)
                page_size -= 1
            nxt_idx += 1
            if nxt_idx >= len(indexed_dataset):
                break
        return {
            'index': index,
            'next_index': nxt_idx,
            'page_size': len(data),
            'data': data
            }
