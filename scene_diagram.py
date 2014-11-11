"""Argand Diagram Plotter

scene_diagram.py - Implements QGraphicsScene for
                   drawing plots axes and labels
                   in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from utils import clamp


CLING_THRES = 10


class SceneDiagram(QGraphicsScene):
    def __init__(self, program):
        super(SceneDiagram, self).__init__()
        self.program = program

    def draw_axes(self, preferences):
        if preferences.label_axes:
            pass

        width = self.sceneRect().width()
        height = self.sceneRect().height()

        origin = -self.program.diagram.translation
        origin.x = clamp(origin.x, CLING_THRES - width / 2, width / 2 - CLING_THRES)
        origin.y = clamp(origin.y, CLING_THRES - height / 2, height / 2 - CLING_THRES)

        self.addLine(width / 2 + origin.x, 0, width / 2 + origin.x, height)
        self.addLine(0, height / 2 + origin.y, width, height / 2 + origin.y)

    def set_viewport(self, viewport):
        self.setSceneRect(QRectF(viewport.geometry()))
        self.clear()
