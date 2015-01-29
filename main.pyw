#!python3
"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from preferences import Preferences
from diagram import Diagram
from window import Window


class Program(QObject):
    diagram_changed = pyqtSignal()
    
    def __init__(self):
        super(Program, self).__init__()
        
        self.app = QApplication(sys.argv)
        icon = QIcon()
        for i in range(16, 33, 8):
            # Load the application icon.
            reader = QImageReader("img/half_disk{}.png".format(i))
            icon.addPixmap(QPixmap(reader.read()))
        self.app.setWindowIcon(icon)
        
        self.new_diagram()
        self.preferences = Preferences()
        self.window = Window(self)

    def new_diagram(self):
        self.diagram = Diagram(self)

        if hasattr(self, "window") and self.window:
            # The window will not have been created
            # the first time this is run.
            self.window.diagram.draw()
        self.diagram_changed.emit()

    def open_diagram(self):
        dialog = QFileDialog(self.window)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.diagram = Diagram(self, dialog.selectedFiles()[0])

        self.window.diagram.draw()
        self.diagram_changed.emit()

    def save_diagram(self):
        if self.diagram:
            self.diagram.save()

    def save_diagram_as(self):
        if self.diagram:
            self.diagram.save_as()
    
    def exec_(self):
        return self.app.exec_()


if __name__ == "__main__":
    program = Program()
    sys.exit(program.exec_())
