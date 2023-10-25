# !/usr/bin/env python3
""" BaseCaching module using FIFO algorithm """
from collections import OrderedDict, Counter


BaseCaching = __import__("base_caching").BaseCaching


# Create a class LFUCache that inherits from BaseCaching system:

# def put(self, key, item):
# you must discard the least frequency used item (LFU algorithm)
# if you find more than 1 item to discard,
# -  you must use the LRU algorithm to discard only the least recently used
# you must print DISCARD: with the key discarded and following by a new line


class LFUCache(BaseCaching):
    """Caching System"""

    def __init__(self):
        """Initiliaze"""
        super().__init__()
        self.cache_data = OrderedDict(self.cache_data)
        self.freq = {}

    def put(self, key, item):
        """Add an item in the cache"""
        if key and item:
            if key in self.cache_data:
                # Update frequency for existing key
                self.frequency_update(self, key)
                self.cache_data[key] = item
                return
            if len(self.cache_data) >= self.MAX_ITEMS:
                # get the lowest freqeuncy from the frequency dict
                items_to_discard = [
                    (self.freq[key], key) for key in self.freq.keys()
                ]
                del_key = sorted(items_to_discard)[0][1]
                del self.cache_data[del_key]
                del self.freq[del_key]
                print("DISCARD: {}".format(del_key))
                # add new item
                self.cache_data[key] = item
                self.freq[key] = 1
            self.cache_data[key] = item
            self.freq[key] = 1

    def get(self, key):
        """Get an item by key"""
        if key in self.cache_data:
            # increase the frequency for that key
            self.frequency_update(self, key)
            return self.cache_data.get(key)
        return None

    @staticmethod
    def frequency_update(self, key):
        """Update the frequency dict"""
        self.freq[key] += 1
