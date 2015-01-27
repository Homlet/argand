"""Argand Diagram Plotter

diagram.py - Stores all information pertaining to
             a single instance of a diagram.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from plot import Plot
from plot_list import PlotListModel
from geometry import Point


class Diagram(QObject):
    zoom_changed = pyqtSignal(float)
    translation_changed = pyqtSignal(Point)

    def __init__(self):
        super(Diagram, self).__init__()
               
        self.plots = PlotListModel()
        self.zoom = 1.0
        self.translation = Point(0.0, 0.0)
        self.filename = None

    def set_zoom(self, value):
        self.zoom = value
        self.zoom_changed.emit(value)

    def set_translation(self, value):
        self.translation = value
        self.translation_changed.emit(value)

    def translate(self, delta):
        self.set_translation(self.translation + delta)

    def save_diagram(self):
        if filename:
            pass
        else:
            self.save_diagram_as()

    def save_diagram_as(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_(self):
            filename = dialog.selectedFiles()[0]
