"""Argand Diagram Plotter

dialog_plots.py - Creates a dockable dialog for creating and
                  managing plots.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from plot_list import *


class DialogPlots(QDockWidget):
    def __init__(self, parent, program):
        super(DialogPlots, self).__init__("Plots", parent)
        self.program = program
        self.setup_content()
        self.initialize()

    def setup_content(self):
        # Setup the container widget.
        self.widget = QWidget()
        self.widget.setMinimumSize(200, 300)

        # Setup the list of plots.
        self.list = PlotListTable(self.program.diagram.plots)
        self.add_plot_button = QPushButton("+")
        self.add_plot_button.clicked.connect(self.add_plot)

        # Setup the equation input.
        self.equation = QLineEdit()
        self.equation.setPlaceholderText("Enter equation...")
        self.equation.setEnabled(False)

        # Create a color picker dialog.
        self.color = QColorDialog()

        # Setup a button to open the color dialog.
        self.color_image = QLabel()
        self.color_image.setPixmap(QPixmap("img/color16.png"))

        self.color_button = QPushButton("Color...")
        self.color_button.clicked.connect(self.change_color)
        self.color_button.setEnabled(False)

        self.color_label = QWidget()

        # Create a slider to control the inequality opacity.
        self.alpha_image = QLabel()
        self.alpha_image.setPixmap(QPixmap("img/alpha16.png"))

        self.alpha = QSlider(Qt.Horizontal)
        self.alpha.setTickPosition(QSlider.TicksBelow)
        self.alpha.setRange(0, 100)
        self.alpha.setValue(100)
        self.alpha.setTickInterval(10)
        self.alpha.valueChanged.connect(self.update_alpha_label)
        self.alpha.setEnabled(False)

        self.alpha_label = QLabel(str(self.alpha.value()))

        # Create a frame for the input area.
        self.input_frame = QFrame()
        self.input_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        input_grid = QGridLayout()
        input_grid.setColumnStretch(2, 0)
        input_grid.setContentsMargins(3, 3, 3, 3)
        self.input_frame.setLayout(input_grid)

        # Add input widgets to the frame.
        input_grid.addWidget(self.equation, 0, 0, 1, 0)
        input_grid.addWidget(self.color_image, 1, 0)
        input_grid.addWidget(self.color_button, 1, 1)
        input_grid.addWidget(self.color_label, 1, 2)
        input_grid.addWidget(self.alpha_image, 2, 0)
        input_grid.addWidget(self.alpha, 2, 1)
        input_grid.addWidget(self.alpha_label, 2, 2)

        # Create a grid layout in the widget.
        grid = QGridLayout()
        grid.setContentsMargins(3, 3, 3, 3)
        self.widget.setLayout(grid)

        # Add everything to the grid.
        grid.addWidget(self.list, 0, 0)
        grid.addWidget(self.add_plot_button, 1, 0)
        grid.addWidget(self.input_frame, 2, 0)

    def initialize(self):
        self.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(self.widget)
        self.input_frame.layout().setColumnMinimumWidth(2, 20)
        
        self.current_plot = None

    def change_color(self):
        """Change the color of the currently selected equation."""
        palette = QPalette()
        palette.setColor(QPalette.Background, self.color.getColor())
        self.color_label.setPalette(palette)
        self.color_label.setAutoFillBackground(True)

    def add_plot(self):
        """Add a new plot to the plot list and select it."""
        pass

    def update_alpha_label(self, value):
        """Changes the alpha label's value to match the alpha slider."""
        self.alpha_label.setText(str(value))
