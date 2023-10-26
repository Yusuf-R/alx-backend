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
        # make sure page_size is an integer and greater than 0
        assert isinstance(page_size, int) and page_size > 0
        # make sure index is an integer and also permit if index is None
        assert isinstance(index, int) or index is None
        # make sure index is within >= 0 < len of dataset
        assert 0 <= index < len(self.dataset())

        # set index to 0 if none was provided
        if index is None:
            index = 0
        # make a copy of this index since we will modify
        # but keep original for data information page
        curr_idx = index

        # get all the indexed_dataset, it is a dictoinary {key:[data]}
        indexed_dataset = self.indexed_dataset()

        # while the page size is greater than 0
        while page_size > 0:
            # get the data at the current index
            data_content = indexed_dataset.get(curr_idx)

            # if the data is not None
            if data_content is not None:

                # store this result in the data list object
                data.append(data_content)

                # decreament size
                page_size -= 1

            # if data_content is None:
            # we move to the next index by adding 1 to our curr
            curr_idx += 1

            # curr idx is > we break out
            if curr_idx >= len(indexed_dataset):
                break

            # return the proper details of the query
            # picture next index as the index of our curr after
            # existing the loop
        return {
            'index': index,
            'next_index': curr_idx,
            'page_size': len(data),
            'data': data
            }
