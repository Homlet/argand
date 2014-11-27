#!python3
"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4.QtGui import *

from preferences import Preferences
from diagram import Diagram
from window import Window


class Program:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QIcon("img/logo16.png"))
        self.diagram = Diagram()
        self.preferences = Preferences()
        self.window = Window(self)

    def exec_(self):
        return self.app.exec_()


if __name__ == "__main__":
    program = Program()
    sys.exit(program.exec_())
