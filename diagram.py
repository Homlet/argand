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
        self.translation = Point(1.0, 5.0)
        
        self.plots.append(Plot("123=235", QColor(200, 200, 0)))
        self.plots.append(Plot("123=2135", QColor(220, 100, 0)))
        self.plots.append(Plot("123=2135", QColor(0, 100, 200)))
        self.plots.append(Plot("123=2135", QColor(220, 10, 0)))
