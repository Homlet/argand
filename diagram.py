"""Argand Diagram Plotter

diagram.py - Stores all information pertaining to
             a single instance of a diagram.

Written by Sam Hubbard - samlhub@gmail.com
"""

import ntpath, pickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from plot import Plot
from plot_list import PlotListModel
from geometry import Point


class Diagram(QObject):
    zoom_changed = pyqtSignal(float)
    translation_changed = pyqtSignal(Point)

    def __init__(self, program, path=None):
        super(Diagram, self).__init__()
        
        self.program = program
        self.path = path
        
        if path:
            self.load(path)
            self.filename = ntpath.basename(path)
        else:
            self.plots = PlotListModel()
            self.zoom = 1.0
            self.translation = Point(0.0, 0.0)
            self.filename = "Untitled"

    def set_zoom(self, value, notify=True):
        self.zoom = value
        if notify:
            self.zoom_changed.emit(value)

    def set_translation(self, value, notify=True):
        self.translation = value
        if notify:
            self.translation_changed.emit(value)

    def translate(self, delta):
        self.set_translation(self.translation + delta)

    def save(self):
        if self.path:
            plot_bytes = QByteArray()
            
            buffer = QBuffer(plot_bytes)
            buffer.open(QIODevice.WriteOnly)
            stream = QDataStream(buffer)
            for plot in self.plots:
                stream << plot
            data = [plot_bytes, self.zoom, self.translation]
            with open(self.path, "wb") as file:
                file.truncate()
                pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
        else:
            self.save_as()

    def save_as(self):
        dialog = QFileDialog(self.program.window)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.selectFile(self.path)
        if dialog.exec_():
            self.path = dialog.selectedFiles()[0]
            self.save()

    def load(self, path):
        with open(path, "rb") as file:
            data = pickle.load(file)
        plot_bytes = data[0]
        
        self.plots = PlotListModel()
        
        buffer = QBuffer(plot_bytes)
        buffer.open(QIODevice.ReadOnly)
        stream = QDataStream(buffer)
        while not stream.atEnd():
            plot = Plot()
            stream >> plot
            self.plots.append(plot)
        self.zoom = data[1]
        self.translation = data[2]
