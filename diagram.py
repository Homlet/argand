"""Argand Diagram Plotter

diagram.py - Stores all information pertaining to
             a single instance of a diagram.

Written by Sam Hubbard - samlhub@gmail.com
"""

from plot import *
from geometry import Point


class Diagram:
    def __init__(self):
        self.plots = [(20, 5)]
        self.zoom = 1.0
        self.translation = Point(20.0, 5.0)
