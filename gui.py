"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

import sys

from PyQt4 import QtGui, QtCore

from dialog_plots import DialogPlots


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setup_content()
        self.create_actions()
        self.setup_menubar()
        self.initialize()

    def setup_content(self):
        # Setup a central container widget.
        self.center = QtGui.QWidget()
        self.setCentralWidget(self.center)

        # Create a grid layout in the central widget.
        self.grid = QtGui.QGridLayout()
        self.grid.setContentsMargins(1, 1, 1, 1)
        self.grid.setSpacing(2)
        self.center.setLayout(self.grid)

        # Add a graphics area for drawing the diagram.
        self.diagram = QtGui.QGraphicsView()
        self.grid.addWidget(self.diagram, 0, 0, 1, 0)

        # Create a control region under the diagram.
        self.position_label = QtGui.QLabel()
        self.position_label.setPixmap(QtGui.QPixmap("img/position16.png"))
        self.grid.addWidget(self.position_label, 1, 1)
        
        self.position_input_x = QtGui.QLineEdit()
        self.position_input_x.setFixedWidth(40)
        self.position_input_x.setAlignment(QtCore.Qt.AlignRight)
        self.grid.addWidget(self.position_input_x, 1, 2)

        self.position_input_y = QtGui.QLineEdit()
        self.position_input_y.setFixedWidth(40)
        self.position_input_y.setAlignment(QtCore.Qt.AlignRight)
        self.grid.addWidget(self.position_input_y, 1, 3)

        # Create a spacer.
        self.grid.setColumnMinimumWidth(4, 5)
        self.grid.setColumnStretch(4, 0)

        self.zoom_label = QtGui.QLabel()
        self.zoom_label.setPixmap(QtGui.QPixmap("img/zoom16.png"))
        self.grid.addWidget(self.zoom_label, 1, 5)

        self.zoom_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.zoom_slider.setFixedWidth(100)
        self.grid.addWidget(self.zoom_slider, 1, 6)

        self.grid.setColumnStretch(0, 1)

        # Add the plot list docking dialog.
        self.plots = DialogPlots(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.plots)

    def create_actions(self):        
        self.a_exit = QtGui.QAction("&Exit", self)
        self.a_exit.setShortcut("Ctrl+W")
        self.a_exit.triggered.connect(QtGui.qApp.quit)

        self.a_toggle_plots = self.plots.toggleViewAction()
        self.a_toggle_plots.setShortcut("Ctrl+P")

    def setup_menubar(self):
        menubar = self.menuBar()
        
        menu_file = menubar.addMenu("&File")
        #menu_file.addAction(self.a_new)
        #menu_file.addAction(self.a_open)
        #menu_file.addAction(self.a_save)
        #menu_file.addAction(self.a_save_as)
        menu_file.addAction(self.a_exit)

        menu_view = menubar.addMenu("&View")
        menu_view.addAction(self.a_toggle_plots)
        #menu_view.addAction(self.a_show_prefs)

        menu_help = menubar.addMenu("&Help")
        #menu_file.addAction(self.a_show_docs)
        #menu_file.addAction(self.a_show_about)
        
    def initialize(self):
        self.setGeometry(200, 150, 800, 600)
        #self.setMinimumSize(640, 480)
        self.setWindowTitle("Argand Diagram Plotter")
        self.show()
