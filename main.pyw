#!python3
"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4.QtGui import *

from preferences import Preferences
from diagram import Diagram
from window import Window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("img/logo16.png"))
    diagram = Diagram()
    preferences = Preferences()
    window = Window(preferences)
    sys.exit(app.exec_())
