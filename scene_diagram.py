"""Argand Diagram Plotter

scene_diagram.py - Implements QGraphicsScene for
                   drawing plots axes and labels
                   in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from plot import *
from geometry import *
from utils import clamp, floor_to


CLING_THRES = 10
LABEL_PAD = 20
TICK_SIZE = 2


class FlippedText(QGraphicsTextItem):
    """A vertically flipped text item.
    
    This is needed for using a properly oriented Cartesian
    coordinate system with QGraphicsScene, unfortunately.
    """
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
    """Implementation of QGraphicsScene for drawing diagrams."""
    def __init__(self, program):
        super(SceneDiagram, self).__init__()
        self.program = program
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

    def draw_axes(self):
        """Draws the real and imaginary axes.
        
        If the current preferences allow it, the axes will
        be labelled. Labels will expand as the zoom increases.
        
        If the axes are too far from the viewport, they will
        'cling' to the edges of the screen, but the labels
        will still change.
        """
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
        
        # Draw the axes.
        self.addLine(width / 2 + cling_x, 0, width / 2 + cling_x, height)
        self.addLine(0, height / 2 + cling_y, width, height / 2 + cling_y)
        
        # If enabled, label the axes.
        if self.program.preferences.label_axes:
            # Draw the Re and Im labels.
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

            # Set the step using the order of magnitude of the current zoom.
            step = 10 ** floor_to(2 - log10(zoom), log10(5))
            pixels = step * zoom

            re_steps = ceil(width / pixels * 0.75)
            for i in range(-re_steps, re_steps):
                if i == 0: continue
                self.addItem(FlippedText(
                    "{:n}".format(i * step),
                    width / 2 + origin.x + i * pixels,
                    height / 2 + cling_y))
                self.addLine(
                    width / 2 + origin.x + i * pixels,
                    height / 2 + cling_y + TICK_SIZE,
                    width / 2 + origin.x + i * pixels,
                    height / 2 + cling_y - TICK_SIZE)

            im_steps = ceil(height / pixels * 0.75)
            for i in range(-im_steps, im_steps):
                if i == 0: continue
                self.addItem(FlippedText(
                    "{:n}".format(i * step),
                    width / 2 + cling_x,
                    height / 2 + origin.y + i * pixels))
                self.addLine(
                    width / 2 + cling_x + TICK_SIZE,
                    height / 2 + origin.y + i * pixels,
                    width / 2 + cling_x - TICK_SIZE,
                    height / 2 + origin.y + i * pixels)

            # Only label origin if it is actually in viewport (not clinging).
            if cling_x - origin.x == 0 and cling_y - origin.y == 0:
                self.addItem(FlippedText(
                    "0",
                    width / 2 + cling_x,
                    height / 2 + cling_y
                ))
    
    def draw_plots(self):
        width = self.sceneRect().width()
        height = self.sceneRect().height()
        
        offset = self.program.diagram.translation
        zoom = self.program.diagram.zoom
        stroke = self.program.preferences.stroke
        
        for i in range(self.program.diagram.plots.rowCount()):
            plot = self.program.diagram.plots.item(i)
            type = plot.data(ROLE_TYPE)
            shape = plot.data(ROLE_SHAPE)
            color = plot.data(ROLE_COLOR)
            
            pen = QPen(color)
            pen.setWidth(stroke)
            
            # TODO: Check if on screen.
            if isinstance(shape, Circle):
                if type == TYPE_CIRCLE:
                    self.addEllipse(
                        width / 2 + (shape.origin().x - offset.x) * zoom,
                        height / 2 + (shape.origin().y - offset.y) * zoom,
                        shape.diameter() * zoom, shape.diameter() * zoom, pen)
                if type == TYPE_DISK:
                    pass
                if type == TYPE_NEGATIVE_DISK:
                    pass

            if isinstance(shape, Line):
                if type == TYPE_LINE:
                    pass
                if type == TYPE_HALF_PLANE:
                    pass

            if isinstance(shape, Ray):
                if type == TYPE_RAY:
                    pass
                if type == TYPE_SECTOR:
                    pass

    def set_viewport(self, viewport):
        """Called when the size of the parent widget changes."""
        self.setSceneRect(QRectF(viewport.geometry()))
