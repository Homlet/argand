"""Argand Diagram Plotter

utils.py - Various utility functions.

Written by Sam Hubbard - samlhub@gmail.com
"""


def clamp(value, low, high):
    return max(low, min(value, high))
