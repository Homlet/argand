"""Argand Diagram Plotter

dialog_plots.py - Creates a dockable dialog for creating and
                  managing plots.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4 import QtGui, QtCore


class DialogPlots(QtGui.QDockWidget):
    def __init__(self, parent):
        super(DialogPlots, self).__init__("Plots", parent)
        self.setup_content()
        self.initialize()

    def setup_content(self):
        # Setup the container widget.
        self.widget = QtGui.QWidget()
        self.widget.setMinimumSize(200, 300)

        # Create a grid layout in the widget.
        self.grid = QtGui.QGridLayout()
        self.grid.setContentsMargins(3, 3, 3, 3)
        self.widget.setLayout(self.grid)

        # Setup the list of plots.
        self.list = QtGui.QListWidget()
        self.grid.addWidget(self.list, 0, 0, 1, 0)

        # Setup the equation input.
        self.equation = QtGui.QLineEdit()
        self.equation.setPlaceholderText("Enter equation...")
        self.grid.addWidget(self.equation, 1, 0, 1, 0)

        # Create a color picker dialog.
        self.color = QtGui.QColorDialog()

        # Setup a button to open the color dialog.
        self.color_label = QtGui.QLabel()
        self.color_label.setPixmap(QtGui.QPixmap("img/color16.png"))
        self.grid.addWidget(self.color_label, 2, 0)
        
        self.color_button = QtGui.QPushButton("Color...")
        self.color_button.clicked.connect(self.change_color)
        self.grid.addWidget(self.color_button, 2, 1, 1, 2)

        # Create a slider to control the inequality opacity.
        self.alpha_image = QtGui.QLabel()
        self.alpha_image.setPixmap(QtGui.QPixmap("img/alpha16.png"))
        self.grid.addWidget(self.alpha_image, 3, 0)
        
        self.alpha = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.alpha.setTickPosition(QtGui.QSlider.TicksBelow)
        self.alpha.setRange(0, 100)
        self.alpha.setTickInterval(10)
        self.alpha.valueChanged.connect(self.update_alpha_label)
        self.grid.addWidget(self.alpha, 3, 1)
        self.grid.setColumnStretch(1, 0)
        
        self.alpha_label = QtGui.QLabel("100")
        self.grid.addWidget(self.alpha_label, 3, 2)

    def initialize(self):
        self.setAllowedAreas(
            QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )
        self.setWidget(self.widget)

    def change_color(self):
        """Changes the color of the currently selected equation."""
        self.color.getColor()

    def update_alpha_label(self, value):
        """Changes the alpha label's value to match the alpha slider."""
        self.alpha_label.setText(str(value))
