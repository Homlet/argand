"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4 import QtGui

from gui import Window


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
