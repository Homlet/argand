"""Argand Diagram Plotter

diagram.py - Stores all information pertaining to
             a single instance of a diagram.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *

from plot import Plot
from geometry import Point


class Diagram:
    def __init__(self):
        self.plots = QStandardItemModel()
        self.plots.appendRow(Plot("4=4"))
        self.plots.appendRow(Plot("456=234+634", QColor(200, 200, 50)))
        self.plots.appendRow(Plot("4=444", QColor(255, 0, 0)))
        self.zoom = 1.0
        self.translation = Point(-1.0, -5.0)
