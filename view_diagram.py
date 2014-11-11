"""Argand Diagram Plotter

view_diagram.py - Implements QGraphicsView for
                  drawing plots axes and labels
                  in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from scene_diagram import SceneDiagram


class ViewDiagram(QGraphicsView):
    def __init__(self, program):
        super(ViewDiagram, self).__init__()
        self.program = program
        self.scene = SceneDiagram(program)
        self.setScene(self.scene)
        self.scale(1, -1)
        
    def resizeEvent(self, event):
        self.scene.set_viewport(self.viewport())
        self.draw()
    
    def draw(self):
        self.scene.clear()
        self.scene.draw_axes()
