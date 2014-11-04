"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4 import QtGui

from window import Window


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    diagram = Diagram()
    window = Window(diagram)
    sys.exit(app.exec_())
