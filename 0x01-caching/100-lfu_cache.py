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
        self.frequency = Counter()

    def print_cache(self):
        """Print the cache content"""
        print("Current cache:")
        for key, (item, _) in self.cache_data.items():
            print("{}: {}".format(key, item))

    def put(self, key, item):  # sourcery skip: extract-method, last-if-guard
        """Add an item in the cache"""
        if key and item:
            if key in self.cache_data:
                # Update frequency for existing key
                _, freq = self.cache_data[key]
                self.frequency[key] += 1
                self.cache_data[key] = (item, freq + 1)
                return

            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.frequency.values())
                items_to_discard = [
                    k for k, v in self.frequency.items() if v == min_freq
                ]
                last_key = min(
                    items_to_discard, key=lambda k: self.frequency[k]
                )

                del self.cache_data[last_key]
                del self.frequency[last_key]
                print("DISCARD: {}".format(last_key))

            self.cache_data[key] = (item, 0)
            self.frequency[key] += 1

    def get(self, key):
        """Get an item by key"""
        if key in self.cache_data:
            # self.cache_data.move_to_end(key)
            # extract the value -> tuple(value, int(freq))
            item, freq = self.cache_data[key]
            # increase the frequency for that key
            self.cache_data[key] = (item, freq + 1)
            # store the key and its frequency in frequency dict
            self.frequency[key] += 1
            return item
        return None
