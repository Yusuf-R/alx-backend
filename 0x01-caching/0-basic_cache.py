#!/usr/bin/env python3
""" Caching System """

BaseCaching = __import__('base_caching').BaseCaching

# Create a class BasicCache that inherits from BaseCaching
# You must use self.cache_data from the parent class BaseCaching
# This caching system doesn’t have limit
# def put(self, key, item):
# assign to the dictionary self.cache_data the item value for the key.
# If key or item is None, this method should not do anything.
# def get(self, key):
# Must return the value in self.cache_data linked to key.
# If key is None or if the key doesn’t exist in self.cache_data, return None.


class BasicCache(BaseCaching):
    """ Caching System """

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key in self.cache_data:
            return self.cache_data.get(key)
        return None
