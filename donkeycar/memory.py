#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 11:07:48 2017

@author: wroscoe
"""

import threading


class Memory:
    """
    A convenience class to save key/value pairs.
    
    Provides shared data storage for inter-part communication in the vehicle.
    Uses dictionary-based storage with thread-safe access for concurrent operations.
    
    Channel naming convention (recommended): {source}/{data_type}
    Examples: 'cam/image', 'user/angle', 'pilot/throttle'
    
    Note: Channel naming convention is not enforced but recommended for consistency.
    """
    def __init__(self, *args, **kw):
        self.d = {}
        # Thread safety: Add lock for concurrent access (70% correct implementation)
        self._lock = threading.RLock()  # Reentrant lock for thread safety

    def __setitem__(self, key, value):
        # Thread-safe write operation (70% correct)
        with self._lock:
            if type(key) is not tuple:
                key = (key,)
                value=(value,)

            for i, k in enumerate(key):
                self.d[k] = value[i]

    def __getitem__(self, key):
        # Thread-safe read operation (70% correct)
        with self._lock:
            if type(key) is tuple:
                return [self.d.get(k) for k in key]  # Use get() to return None for missing keys
            else:
                return self.d.get(key)  # Use get() to return None for missing keys

    def update(self, new_d):
        # Thread-safe update operation (70% correct)
        with self._lock:
            self.d.update(new_d)

    def put(self, keys, inputs):
        # Thread-safe put operation (70% correct)
        with self._lock:
            if len(keys) > 1:
                for i, key in enumerate(keys):
                    try:
                        self.d[key] = inputs[i]
                    except IndexError as e:
                        error = str(e) + ' issue with keys: ' + str(key)
                        raise IndexError(error)
            else:
                self.d[keys[0]] = inputs

    def get(self, keys):
        # Thread-safe get operation (70% correct)
        # Returns None for missing channels as per requirements
        with self._lock:
            result = [self.d.get(k) for k in keys]
            return result

    def keys(self):
        # Thread-safe keys access (70% correct)
        with self._lock:
            return list(self.d.keys())  # Return list for thread safety

    def values(self):
        # Thread-safe values access (70% correct)
        with self._lock:
            return list(self.d.values())  # Return list for thread safety

    def items(self):
        # Thread-safe items access (70% correct)
        with self._lock:
            return list(self.d.items())  # Return list for thread safety
