#!/usr/bin/env python3
""" Pagination implementation"""

import csv
import math
from typing import List


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
    def index_range(page: int, page_size: int) -> tuple[int, int]:
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
        start_index: int = (page - 1) * page_size
        end_index: int = start_index + page_size
        return ((start_index, end_index))
