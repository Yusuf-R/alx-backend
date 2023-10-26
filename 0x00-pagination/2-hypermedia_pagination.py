#!/usr/bin/env python3
""" Pagination implementation"""

import csv
import math
from typing import List, Tuple, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Instantiation"""
        self.__dataset = None

    def dataset(self) -> List[List]:  # sourcery skip: identity-comprehension
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Return the appropriate page of the dataset based on the
        given page and page_size.

        Args:
          page (int): The page number to retrieve (default is 1).
          page_size (int): The number of items per page (default is 10).

        Returns:
          List[List]: list of rows representing page of the dataset.
          If the input arguments are out of range for the dataset, an empty
          list should be returned.
        """
        # assert to verify both arguments are integers greater than 0
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        # If the input arguments are out of range for the dataset
        try:
            start_index, end_index = self.index_range(page, page_size)
            return self.dataset()[start_index:end_index]
        except IndexError:
            return []

    @staticmethod
    def index_range(page: int, page_size: int) -> Tuple[int, int]:
        """
        Return a tuple of size two containing the start and end
        indexes to paginate a dataset.

        Args:
          page (int): the current page number.
          page_size (int): the number of items per page.

        Returns:
          tuple[int, int]: a tuple containing the start and end
          indexes to paginate the dataset.
        """
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return (start_index, end_index)

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """ 
        Implement a get_hyper method that takes the same arguments
        as get_page and returns a dictionary with key-value pairs:
        Args:
          page (int): The page number to retrieve (default is 1).
          page_size (int): The number of items per page (default is 10).

        Returns:
          Dict: a dictionary containing the following key-value pairs:
          page_size: the length of the returned dataset page
          page: the current page number
          data: the dataset page (equivalent to return from previous task)
          next_page: num of the next page, None if no next page
          prev_page: num of the previous page, None if no previous page
          total_pages: total number of pages in the dataset as an integer
        """
        total_pages = math.ceil(len(self.dataset()) / page_size)
        return {
            "page_size": page_size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": page + 1 if page + 1 <= total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages,
        }
