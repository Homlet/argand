"""Diagram View

Implementation of QGraphicsView for drawing plots
axes and labels in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
Copyright (C) 2015 Sam Hubbard
"""

from PySide.QtGui import *
from PySide.QtCore import *

from geometry import Point
from scene_diagram import SceneDiagram


class ViewDiagram(QGraphicsView):
    """Implementation of QGraphicsView for handling a diagram QGraphicsScene.
    
    Attributes:
        program: Reference to the program object.
        scene: Reference to the QGraphicsScene.
        dragging: True if the user is currently dragging over the view.
        last_pos: The last position where the mouse was down.
    """
    def __init__(self, program):
        """Create the view.
        
        Args:
            program: See ViewDiagram.program.
        """
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
        """Clear the scene and signal the it to re-draw itself."""
        self.scene.clear()
        self.scene.draw_axes()
        self.scene.draw_plots()
        # Force the scene to repaint now, rather than at the end
        # of the event queue.
        self.viewport().repaint()

    def mousePressEvent(self, event):
        """Start dragging when the mouse button is pressed."""
        self.dragging = True
        self.last_pos = Point(event.x(), self.viewport().height() - event.y())
        super(ViewDiagram, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle dragging when the mouse is down and moving over the view."""
        if self.dragging:
            zoom = self.program.diagram.zoom
            mouse_pos = Point(event.x(), self.viewport().height() - event.y())
            delta = (mouse_pos - self.last_pos) * (1 / zoom)
            self.last_pos = mouse_pos

            self.program.diagram.translate(-delta)
            self.draw()
        super(ViewDiagram, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Stop dragging when the mouse button is released."""
        self.dragging = False
        super(ViewDiagram, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """Handle zooming when the user scrolls the mouse wheel."""
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
        """Resize the viewport when the window is resized."""
        self.scene.set_viewport(self.viewport())
        self.draw()
