"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4 import QtGui

from window import Window
from diagram import Diagram


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    diagram = Diagram()
    window = Window()
    sys.exit(app.exec_())
