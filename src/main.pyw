#!python3
"""Argand Plotter

Argand Plotter is a program for drawing Argand Diagrams.
The program was written as a project for A2 computing coursework.

Written by Sam Hubbard - samlhub@gmail.com
Copyright (C) 2015 Sam Hubbard
"""

import sys, os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from preferences import Preferences
from diagram import Diagram
from window import Window


class Program(QObject):
    """Simple class to hold all components of the program.
       This must extend QObject so that PyQt signals can be used.
    """
    diagram_changed = pyqtSignal()
    
    def __init__(self, path=None):
        """Create and initialise all components of the program.
           If path is given, load the referenced argand file,
           otherwise create a new blank file.

           diagram     - A Diagram object which holds the current display
                         transformation as well as the list of plots to draw.

           window      - A QMainWindow which serves as the main handle to
                         the entire PyQt GUI.

           preferences - Stores a few diagram-independent settings.
        """
        super(Program, self).__init__()

        # Create the application.
        self.app = QApplication(sys.argv)
        icon = QIcon()
        for i in [16, 24, 32, 64, 128]:
            # Load the application icon.
            img = self.get_path("img/half_disk{}.png".format(i))
            reader = QImageReader(img)
            icon.addPixmap(QPixmap(reader.read()))
        self.app.setWindowIcon(icon)

        # Initialise modules.
        if path:
            print(path)
            self.open_diagram(path)
        else:
            self.new_diagram()
        self.preferences = Preferences()
        self.window = Window(self)
        self.diagram_changed.emit()

    def new_diagram(self):
        """Create a new blank diagram object. If the window exists at
           this point, redraw the diagram.
        """
        self.diagram = Diagram(self)

        if hasattr(self, "window") and self.window:
            # The window will not have been created
            # the first time this is run.
            self.window.diagram.draw()
        self.diagram_changed.emit()

    def open_diagram(self, path=None):
        """Open the file at path. If no path is given, prompt
           the user for a .arg file to open.

           On confirmation, create a new diagram and load
           the file into it.
        """
        # If path not given, prompt the user for one.
        if not path:
            dialog = QFileDialog(self.window)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.setViewMode(QFileDialog.Detail)
            dialog.setNameFilter("Argand Plotter Diagrams (*.arg)")
            if dialog.exec_():
                path = dialog.selectedFiles()[0]

        # Check again, as path may have been set.
        if path:
            self.diagram = Diagram(self, path)

            if hasattr(self, "window") and self.window:
                # The window may not have been created
                # the first time open is run.
                self.window.diagram.draw()
            self.diagram_changed.emit()

    def save_diagram(self):
        """Wrapper of diagram save function so as to prevent
           menu actions having to be rebound every time the diagram
           is changed.
        """
        if hasattr(self, "diagram") and self.diagram:
            self.diagram.save()

    def save_diagram_as(self):
        """Wrapper of diagram save_as function so as to prevent
           menu actions having to be rebound every time the diagram
           is changed.
        """
        if hasattr(self, "diagram") and self.diagram:
            self.diagram.save_as()

    def get_path(self, relative):
        """Returns the correct path to a relative file, depending
           on whether the program is running in an interpreter
           or as an executable.
        """
        if getattr(sys, "frozen", False):
            # The application is frozen.
            directory = os.path.dirname(sys.executable)
            return os.path.join(directory, relative)
        else:
            # The application is running in the interpreter.
            return relative
    
    def exec_(self):
        """Begin execution of Qt code (bar initialisation code).
           This essentially bootstraps the entire program.
        """
        return self.app.exec_()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        program = Program(sys.argv[1])
    else:
        program = Program()
    sys.exit(program.exec_())
