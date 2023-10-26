#!/usr/bin/env python3
""" Pagination implementation"""
from typing import Tuple
# Write a function named index_range that takes
# two integer arguments page and page_size.

# The function return a tuple of size two containing a start index
# and an end index corresponding to the range of indexes to return
# in a list for those particular pagination parameters.

# Page numbers are 1-indexed, i.e. the first page is page 1.


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
    start_index: int = (page - 1) * page_size
    end_index: int = start_index + page_size
    return ((start_index, end_index))
