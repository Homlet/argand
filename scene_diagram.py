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
LABEL_PAD = 20


class FlippedText(QGraphicsTextItem):
    def __init__(self, text, x, y):
        super(FlippedText, self).__init__()
        self.setPos(x, y)
        self.setPlainText(text)
        h_width = self.boundingRect().width() / 2
        h_height = self.boundingRect().height() / 2
        transform = QTransform()
        transform.translate(h_width, h_height)
        transform.scale(1, -1)
        transform.translate(-h_width, -h_height)
        self.setTransform(transform)


class SceneDiagram(QGraphicsScene):
    def __init__(self, program):
        super(SceneDiagram, self).__init__()
        self.program = program

    def draw_axes(self):
        width = self.sceneRect().width()
        height = self.sceneRect().height()

        origin = -self.program.diagram.translation * self.program.diagram.zoom
        origin.x = clamp(origin.x, CLING_THRES - width / 2, width / 2 - CLING_THRES)
        origin.y = clamp(origin.y, CLING_THRES - height / 2, height / 2 - CLING_THRES)

        self.addLine(width / 2 + origin.x, 0, width / 2 + origin.x, height)
        self.addLine(0, height / 2 + origin.y, width, height / 2 + origin.y)
        if self.program.preferences.label_axes:
            self.addItem(FlippedText("Re", width - LABEL_PAD, height / 2 + origin.y))
            self.addItem(FlippedText("Im", width / 2 + origin.x, height - LABEL_PAD))

    def set_viewport(self, viewport):
        self.setSceneRect(QRectF(viewport.geometry()))
