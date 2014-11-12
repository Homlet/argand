"""Argand Diagram Plotter

scene_diagram.py - Implements QGraphicsScene for
                   drawing plots axes and labels
                   in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import log

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from utils import clamp


CLING_THRES = 10
LABEL_PAD = 20
LABEL_SPACING = 100


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

        translation = self.program.diagram.translation
        zoom = self.program.diagram.zoom
        origin = -translation * zoom
        
        # Clamp coordinates so the axes cling to the edge of the screen.
        cling_x = clamp(
            origin.x,
            CLING_THRES - width / 2,
            width / 2 - CLING_THRES
        )
        cling_y = clamp(
            origin.y,
            CLING_THRES - height / 2,
            height / 2 - CLING_THRES
        )

        self.addLine(width / 2 + cling_x, 0, width / 2 + cling_x, height)
        self.addLine(0, height / 2 + cling_y, width, height / 2 + cling_y)
        if self.program.preferences.label_axes:
            self.addItem(FlippedText(
                "Re",
                width - LABEL_PAD,
                height / 2 + cling_y - 2 * CLING_THRES
            ))
            self.addItem(FlippedText(
                "Im",
                width / 2 + cling_x - 2 * CLING_THRES,
                height - LABEL_PAD
            ))
            
            # Set the style of label based on how zoomed in we are.
            if zoom >= 1000 * LABEL_SPACING:
                form = "{:.2e}"
            elif zoom >= LABEL_SPACING:
                form = "{:." + str(int(log(zoom))-3) + "f}"
            else:
                form = "{:.0f}"
            
            horizontal_steps = int(width / LABEL_SPACING)
            for i in range(-horizontal_steps, horizontal_steps):
                self.addItem(FlippedText(
                    form.format(i * LABEL_SPACING / zoom),
                    width / 2 + cling_x + i * LABEL_SPACING,
                    height / 2 + cling_y
                ))
            
            vertical_steps = int(height / LABEL_SPACING)
            for i in range(-vertical_steps, vertical_steps):
                self.addItem(FlippedText(
                    form.format(i * LABEL_SPACING / zoom),
                    width / 2 + cling_x,
                    height / 2 + cling_y + i * LABEL_SPACING
                ))

    def set_viewport(self, viewport):
        self.setSceneRect(QRectF(viewport.geometry()))
