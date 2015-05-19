"""Argand Plotter

Argand Plotter is a program for drawing Argand Diagrams.
The program was written as a project for A2 computing coursework.

Written by Sam Hubbard - samlhub@gmail.com
Copyright (C) 2015 Sam Hubbard
"""

import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

from preferences import Preferences
from diagram import Diagram
from window import Window


class Program(QObject):
    """Simple class to hold all components of the program.
    
    This must extend QObject so that PyQt signals can be used.

    Attributes:
        diagram: Holds the display transformation and the list of plots.
        diagram_changed: A signal emitted whenever a new diagram is loaded.
        preferences: Stores a few diagram-independent settings.
        window: Serves as the main handle to the entire PyQt GUI.
    """
    diagram_changed = Signal()
    
    def __init__(self, path=None):
        """Create and initialise all components of the program.

        If path is given, load the referenced .arg file,
        otherwise create a new blank file.
        
        Args:
            path: An optional path to a .arg file to open
        """
        super(Program, self).__init__()

        # Create the application.
        self.app = QApplication(sys.argv)
        icon = QIcon()
        for i in [16, 24, 32, 64, 128]:
            # Load the icon in parts because PyQt has issues
            # loading .ico format icons.
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
        self.diagram.notify_transformation()

    def new_diagram(self):
        """Create a new blank diagram object.

        If the window exists at this point, redraw the diagram.
        """
        self.diagram = Diagram(self)

        if hasattr(self, "window") and self.window:
            # The window will not have been created
            # the first time this is run.
            self.window.diagram.draw()
        self.diagram_changed.emit()
        self.diagram.notify_transformation()

    def open_diagram(self, path=None):
        """Open a .arg file.
        
        If no path is given, prompt the user for a .arg file
        to open. On confirmation, create a new diagram and load
        the file into it.

        Args:
            path: An optional path to a .arg file to open.
        """
        # If path not given, prompt the user for one.
        if not path:
            dialog = QFileDialog(self.window)
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.setViewMode(QFileDialog.Detail)
            dialog.setNameFilter(
                "Argand Plotter Diagrams (*.arg);;" \
                "All Files (*.*)")
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
            self.diagram.notify_transformation()

    def save_diagram(self):
        """Wrapper of diagram save function.
        
        Used to to prevent menu actions having to be rebound
        every time the diagram is changed.
        """
        if hasattr(self, "diagram") and self.diagram:
            self.diagram.save()

    def save_diagram_as(self):
        """Wrapper of diagram save_as function.
        
        Used to to prevent menu actions having to be rebound
        every time the diagram is changed.
        """
        if hasattr(self, "diagram") and self.diagram:
            self.diagram.save_as()
            self.diagram_changed.emit()

    def get_path(self, path):
        """Returns the correct path to a relative file.
        
        This depends on whether the program is running in an
        interpreter or as an executable.
        
        Args:
            path: The relative path to resolve.
        """
        if getattr(sys, "frozen", False):
            # The application is frozen (i.e. is an executable).
            directory = os.path.dirname(sys.executable)
            return os.path.join(directory, path)
        else:
            # The application is running in the interpreter.
            return path
    
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
