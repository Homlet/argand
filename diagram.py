"""Argand Diagram Plotter

diagram.py - Stores all information pertaining to
             a single instance of a diagram.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *

from plot import Plot
from plot_list import PlotListModel
from geometry import Point


class Diagram:
    def __init__(self):
        self.plots = PlotListModel()
        self.zoom = 1.0
        self.translation = Point(-1.0, -5.0)
