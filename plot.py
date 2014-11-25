"""Argand Diagram Plotter

plot.py - Class for storing a single drawable plot.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from abstract_syntax_tree import SyntaxParser


TYPE_CIRCLE = 0
TYPE_DISK = 1
TYPE_NEGATIVE_DISK = 2

TYPE_LINE = 3
TYPE_HALF_PLANE = 4

TYPE_RAY = 5
TYPE_SECTOR = 6

ROLE_EQUATION = Qt.UserRole
ROLE_COLOR = Qt.UserRole + 1
ROLE_BUTTON_STATE = Qt.UserRole + 2

STATE_NORMAL = 0
STATE_HOVER = 1
STATE_DOWN = 2


class Plot(QStandardItem):
    def __init__(self, equation, color=QColor(0, 0, 0)):
        super(Plot, self).__init__()

        self.setData(equation, ROLE_EQUATION)
        self.setData(color, ROLE_COLOR)
        
        self.parser = SyntaxParser(equation)
