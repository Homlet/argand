"""Argand Diagram Plotter

view_diagram.py - Implements QGraphicsView for
                  drawing plots axes and labels
                  in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from geometry import Point
from scene_diagram import SceneDiagram


class ViewDiagram(QGraphicsView):
    def __init__(self, program):
        super(ViewDiagram, self).__init__()
        self.program = program
        self.scene = SceneDiagram(program)
        self.setScene(self.scene)
        
        self.scale(1, -1)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.NoViewportUpdate)
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        self.dragging = False
        self.last_pos = Point(0, 0)
    
    def draw(self):
        self.scene.clear()
        self.scene.draw_axes()
        self.scene.draw_plots()
        self.viewport().repaint()

    def mousePressEvent(self, event):
        self.dragging = True
        self.last_pos = Point(event.x(), self.viewport().height() - event.y())
        super(ViewDiagram, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            zoom = self.program.diagram.zoom
            mouse_pos = Point(event.x(), self.viewport().height() - event.y())
            delta = (mouse_pos - self.last_pos) * (1 / zoom)
            self.last_pos = mouse_pos

            self.program.diagram.translate(-delta)
            self.draw()
        super(ViewDiagram, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        super(ViewDiagram, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        delta = event.delta()
        zoom = self.program.diagram.zoom
        while delta >= 120:
            zoom *= 1.2
            delta -= 120
        while delta <= -120:
            zoom /= 1.2
            delta += 120
        self.program.diagram.set_zoom(zoom)
        self.draw()
        super(ViewDiagram, self).wheelEvent(event)
        
    def resizeEvent(self, event):
        self.scene.set_viewport(self.viewport())
        self.draw()
