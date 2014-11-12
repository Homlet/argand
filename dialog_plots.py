"""Argand Diagram Plotter

dialog_plots.py - Creates a dockable dialog for creating and
                  managing plots.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class DialogPlots(QDockWidget):
    def __init__(self, parent):
        super(DialogPlots, self).__init__("Plots", parent)
        self.setup_content()
        self.initialize()

    def setup_content(self):
        # Setup the container widget.
        self.widget = QWidget()
        self.widget.setMinimumSize(200, 300)

        # Setup the list of plots.
        self.list = QListWidget()

        # Setup the equation input.
        self.equation = QLineEdit()
        self.equation.setPlaceholderText("Enter equation...")

        # Create a color picker dialog.
        self.color = QColorDialog()

        # Setup a button to open the color dialog.
        self.color_label = QLabel()
        self.color_label.setPixmap(QPixmap("img/color16.png"))
        
        self.color_button = QPushButton("Color...")
        self.color_button.clicked.connect(self.change_color)

        # Create a slider to control the inequality opacity.
        self.alpha_image = QLabel()
        self.alpha_image.setPixmap(QPixmap("img/alpha16.png"))
        
        self.alpha = QSlider(Qt.Horizontal)
        self.alpha.setTickPosition(QSlider.TicksBelow)
        self.alpha.setRange(0, 100)
        self.alpha.setTickInterval(10)
        self.alpha.valueChanged.connect(self.update_alpha_label)
        
        self.alpha_label = QLabel("100")

        # Create a grid layout in the widget.
        self.grid = QGridLayout()
        self.grid.setContentsMargins(3, 3, 3, 3)
        self.widget.setLayout(self.grid)
        
        # Add everything to the grid.
        self.grid.addWidget(self.list, 0, 0, 1, 0)
        self.grid.addWidget(self.equation, 1, 0, 1, 0)
        self.grid.addWidget(self.color_label, 2, 0)
        self.grid.addWidget(self.color_button, 2, 1, 1, 2)
        self.grid.addWidget(self.alpha_image, 3, 0)
        self.grid.addWidget(self.alpha, 3, 1)
        self.grid.addWidget(self.alpha_label, 3, 2)

    def initialize(self):
        self.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea
        )
        self.setWidget(self.widget)

    def change_color(self):
        """Changes the color of the currently selected equation."""
        self.color.getColor()

    def update_alpha_label(self, value):
        """Changes the alpha label's value to match the alpha slider."""
        self.alpha_label.setText(str(value))
