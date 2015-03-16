"""Utilities

Various utility functions.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import floor


def clamp(value, low, high):
    """Return value clamped to interval [low, high]."""
    return max(low, min(value, high))


def floor_to(value, interval):
    """Return value rounded down to the nearest multiple of interval."""
    return floor(value / interval) * interval


def ceil_to(value, interval):
    """Return value rounded up to the nearest multiple of interval."""
    return floor_to(value + interval, interval)
