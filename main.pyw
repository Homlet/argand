#!python3
"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys, cpickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from preferences import Preferences
from diagram import Diagram
from window import Window


class Program:
    def __init__(self):
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
        self.diagram = Diagram()

    def open_diagram(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QF
        self.diagram = cpickle.load(
    
    def exec_(self):
        return self.app.exec_()


if __name__ == "__main__":
    program = Program()
    sys.exit(program.exec_())
