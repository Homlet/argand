"""Argand Diagram Plotter

scene_diagram.py - Implements QGraphicsScene for
                   drawing plots axes and labels
                   in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SceneDiagram(QGraphicsScene):
    def __init__(self):
        super(SceneDiagram, self).__init__()
        self.addText("Hello, world!")
