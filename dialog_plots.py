"""Argand Diagram Plotter

dialog_plots.py - Creates a dockable dialog for creating and
                  managing plots.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from plot import *
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
        self.list.selectionModel().selectionChanged.connect(self.plot_changed)

        # Create a button for adding new plots.
        self.add_plot_button = QPushButton("+")
        self.add_plot_button.clicked.connect(self.add_plot)

        # Setup the equation input.
        self.equation = QLineEdit()
        font = QApplication.font()
        font.setPointSize(11)
        self.equation.setFont(font)
        self.equation.setPlaceholderText("Enter equation...")
        self.equation.textChanged.connect(self.equation_changed)
        self.equation_movie = QLabel()
        self.equation_movie.setMovie(QMovie("img/loader16.gif"))
        self.equation_movie.movie().start()
        self.equation_validator = EquationValidator()

        # Setup a button to open the color dialog.
        self.color_label = QWidget()
        self.color_label.setFixedHeight(20)

        self.color_button = QPushButton("...")
        self.color_button.clicked.connect(self.change_color)
        self.color_button.setFixedWidth(26)

        # Create a frame for the input area.
        self.input_frame = QFrame()
        self.input_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.input_frame.setEnabled(False)
        input_grid = QGridLayout()
        input_grid.setColumnStretch(0, 1)
        input_grid.setContentsMargins(3, 3, 3, 3)
        self.input_frame.setLayout(input_grid)

        # Add input widgets to the frame.
        input_grid.addWidget(self.equation, 0, 0, 1, 0)
        input_grid.addWidget(self.equation_movie, 0, 1, Qt.AlignCenter)
        input_grid.addWidget(self.color_label, 1, 0)
        input_grid.addWidget(self.color_button, 1, 1)

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

        self.current_plot = None

    def change_color(self):
        """Change the color of the currently selected equation."""
        if self.current_plot:
            color = QColorDialog.getColor(
                QColor(), self, "Select Color", QColorDialog.ShowAlphaChannel)
            self.change_color_label(color)
            self.list.model().setData(self.current_plot, color, ROLE_COLOR)

    def change_color_label(self, color):
        """Change the color of the label in the input area."""
        self.color_label.setPalette(QPalette(color))
        self.color_label.setAutoFillBackground(True)

    def reset_color_label(self):
        """Set the color label to transparent."""
        self.change_color_label(QColor(0, 0, 0, 0))

    def add_plot(self):
        """Add a new plot to the plot list and select it."""
        plot = Plot("333=3")
        self.list.append(plot)
        index = self.list.model().indexFromItem(plot)
        self.list.clearSelection()
        self.list.selectionModel().select(index,
            QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def plot_changed(self, selected, deselected):
        """Update the current plot attributes.
           Enable the input area if the selection is valid."""
        indexes = selected.indexes()
        valid = len(indexes) > 0

        if valid:
            self.current_plot = indexes[0]
            self.equation.setText(self.current_plot.data(ROLE_EQUATION))
            self.change_color_label(self.current_plot.data(ROLE_COLOR))
        else:
            self.current_plot = None
            self.equation.clear()
            self.reset_color_label()
        self.input_frame.setEnabled(valid)

    def equation_changed(self, text):
        self.equation.valid = self.equation_validator.validate(text, 0)[0]        
        if self.current_plot:
            if self.equation.valid == QValidator.Acceptable:
                color = QApplication.palette().color(QPalette.Base)
                self.list.model().setData(self.current_plot,
                    text, ROLE_EQUATION)
            else:
                color = QColor(250, 180, 180)
        else:
            color = QApplication.palette().color(QPalette.Base)

        palette = QPalette()
        palette.setColor(QPalette.Base, color)
        self.equation.setPalette(palette)

class EquationValidator(QValidator):
    def __init__(self):
        super(EquationValidator, self).__init__()

    def validate(self, input, pos):
        try:
            if SyntaxParser(input).get_tree():
                return (QValidator.Acceptable, input, pos)
        except: pass
        return (QValidator.Intermediate, input, pos)
