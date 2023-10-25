# !/usr/bin/env python3
""" BaseCaching module using FIFO algorithm """
from collections import OrderedDict


BaseCaching = __import__('base_caching').BaseCaching


# Create a class LIFOCache that inherits from BaseCaching system:

# You must use self.cache_data - dictionary from the base BaseCaching
# You can overload def __init__(self)
# def put(self, key, item):
# assign to the dictionary self.cache_data the item value for the key.
# If key or item is None, this method should not do anything.
# If items in self.cache_data is higher that BaseCaching.MAX_ITEMS:
# you must discard the least recently used item (LRU algorithm)
# print DISCARD: with the key discarded and following by a new line
# def get(self, key):
# Must return the value in self.cache_data linked to key.
# If key is None return None.


class MRUCache(BaseCaching):
    """ Caching System """

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()
        self.cache_data = OrderedDict(self.cache_data)

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            # check if the number of item is higher than MAX_ITEMS

            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # discard the first item put in cache
                last_key, _ = self.cache_data.popitem(last=True)
                self.cache_data[key] = item
                print("DISCARD: {}".format(last_key))
                return
            self.cache_data[key] = item

    def get(self, key):  # sourcery skip: assign-if-exp, reintroduce-else
        """ Get an item by key
        """
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
            return self.cache_data.get(key)
        return None
