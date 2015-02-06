"""Diagram

A Diagram object stores the current display transformation,
and the current list of plots to be drawn.

Written by Sam Hubbard - samlhub@gmail.com
Copyright (C) 2015 Sam Hubbard
"""

import ntpath
import pickle
from math import log10

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from plot import Plot
from plot_list import PlotListModel
from geometry import Point


class Diagram(QObject):
    """Stores data about the currently loaded diagram.
    
    This includes the current display transformation, and the current 
    list model of plot objects to be drawn.
    
    Also handles the serialisation / de-serialisation of .arg files.
    
    Attributes:
        program: Reference to the program object.
        path: Path to the associated .arg file (including filename).
        filename: Name of the associated .arg file.
        plots: QModel object containing plots to be drawn.
        zoom: Current display zoom factor.
        zoom_changed: Signal emitted whenever zoom changes.
        translation: Current display pan offset.
        translation_changed: Signal emitted whenever translation changes.
    """
    zoom_changed = pyqtSignal(float)
    translation_changed = pyqtSignal(Point)

    def __init__(self, program, path=None):
        """Create a new Diagram object.
        
        If a path is supplied, the diagram is loaded from that
        file. Otherwise a new blank Diagram object is created.
        
        Args:
            program: See Diagram.program.
            path: See Diagram.path.
        """
        super(Diagram, self).__init__()
        
        self.program = program
        self.path = path
        
        if path:
            # Load the diagram from file.
            self.load(path)
            self.filename = ntpath.basename(path)
        else:
            # Create a new blank diagram.
            self.plots = PlotListModel()
            self.zoom = 1.0
            self.translation = Point(0.0, 0.0)
            self.filename = "Untitled"

    def set_zoom(self, value, notify=True):
        """Set the zoom value, if it lies within the valid range.
        
        Args:
            value: Target value for zoom.
            notify: Whether the zoom_changed signal should be emitted.
        """
        if -50 <= 25 * log10(value) <= 100:
            self.zoom = value
            if notify:
                self.zoom_changed.emit(value)

    def set_translation(self, value, notify=True):
        """Set the translation value.
        
        Args:
            value: Target value for translation.
            notify: Whether the translation_changed signal should be emitted.
        """
        self.translation = value
        if notify:
            self.translation_changed.emit(value)

    def translate(self, delta, notify=True):
        """Offset the translation by some delta.
        
        Args:
            delta: Amount to offset the translation by.
            notify: Whether the translation_changed signal should be emitted.
        """
        self.set_translation(self.translation + delta, notify)
        

    def save(self):
        """Serialise the diagram and save to file.
        
        If the diagram has a path set, serialise the diagram and write to
        that file. Otherwise run Diagram.save_as to prompt the user for
        a path.
        """
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
                pickle.dump(data, file, 3)
        else:
            self.save_as()

    def save_as(self):
        """Prompt the user for a file to save to.
        
        Use the PyQt file dialog to prompt the user for a path. If
        successful, run Diagram.save to serialise and write to that file.
        """
        dialog = QFileDialog(self.program.window)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.selectFile(self.path)
        if dialog.exec_():
            self.path = dialog.selectedFiles()[0]
            self.save()

    def load(self, path):
        """Load the diagram from a file.
        
        Read a .arg file, de-serialise it and load the data into digram.
        
        Args:
            path: See Diagram.path.
        """
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
