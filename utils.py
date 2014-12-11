"""Argand Diagram Plotter

utils.py - Various utility functions.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import floor


def clamp(value, low, high):
    return max(low, min(value, high))


def floor_to(value, interval):
    return floor(value / interval) * interval


def ceil_to(value, interval):
    return floor_to(value + interval, interval)
