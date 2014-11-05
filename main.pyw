"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4.QtGui import *

from window import Window
from diagram import Diagram


if __name__ == "__main__":
    app = QApplication(sys.argv)
    diagram = Diagram()
    window = Window()
    sys.exit(app.exec_())
