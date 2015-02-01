"""Argand Diagram Plotter

dialog_plots.py - Creates a dockable dialog for creating and
                  managing plots.

Written by Sam Hubbard - samlhub@gmail.com
"""

from time import time

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from plot import *
from plot_list import *
from abstract_syntax_tree import SyntaxParser


VALIDATION_DELAY = 0


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
        self.program.diagram_changed.connect(self.set_list_model)

        # Create a button for adding new plots.
        self.add_plot_button = QPushButton("+")
        self.add_plot_button.clicked.connect(self.add_plot)

        # Setup the equation input.
        self.equation = QLineEdit()
        font = QApplication.font()
        font.setPointSize(11)
        self.equation.setFont(font)
        self.equation.setFrame(False)
        self.equation.textChanged.connect(self.equation_changed)

        # Create objects for validating the input.
        self.validation_indicator = QLabel()
        self.validation_indicator.setMovie(QMovie("img/loader16.gif"))
        self.validation_indicator.movie().start()
        self.validation_indicator.setVisible(False)

        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.validate)

        # Set the standard colors in the QColorDialog.
        index = 0
        for i in range(0, 16):
            h = i * 22.5
            for j in range(0, 3):
                s = 255 - j * 20
                v = 255 - j * 65
                QColorDialog.setStandardColor(index,
                    QColor.fromHsv(h, s, v).rgb())
                index += 1
            index += 3
            if index >= 48:
                index = (index % 48) + 3

        # Setup a button to open the color dialog.
        self.color_label = QWidget()
        self.color_label.setFixedHeight(20)

        self.color_button = QPushButton()
        color_button_pixmap = QPixmap("img/color16.png")
        color_button_icon = QIcon(color_button_pixmap)
        self.color_button.setIcon(color_button_icon)
        self.color_button.setIconSize(color_button_pixmap.rect().size())
        self.color_button.clicked.connect(self.change_color)

        # Create a frame for the input area.
        self.input_frame = QFrame()
        self.input_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.input_frame.setEnabled(False)
        input_grid = QGridLayout()
        input_grid.setColumnStretch(0, 1)
        input_grid.setContentsMargins(3, 3, 4, 3)
        input_grid.setSpacing(2)
        self.input_frame.setLayout(input_grid)

        # Add input widgets to the frame.
        input_grid.addWidget(self.equation, 0, 0, 1, 0)
        input_grid.addWidget(self.validation_indicator, 0, 1, Qt.AlignCenter)
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

    def set_list_model(self):
        self.list.setModel(self.program.diagram.plots)
        self.list.selectionModel().selectionChanged.connect(self.plot_changed)
        self.current_plot = None
        self.plot_changed(None, None)

    def change_color(self):
        """Change the color of the currently selected equation."""
        if self.current_plot:
            old_color = self.current_plot.data(ROLE_COLOR)
            color = QColorDialog.getColor(old_color, self, "Select Color",
                QColorDialog.ShowAlphaChannel)
            if color.isValid():
                self.change_color_label(color)
                self.list.model().setData(self.current_plot, color, ROLE_COLOR)
                self.program.window.diagram.draw()

    def change_color_label(self, color):
        """Change the color of the label in the input area."""
        color = QColor(color.rgb())
        self.color_label.setPalette(QPalette(color))
        self.color_label.setAutoFillBackground(True)

    def reset_color_label(self):
        """Set the color label to transparent."""
        self.color_label.setAutoFillBackground(False)

    def add_plot(self):
        """Add a new plot to the plot list and select it."""
        self.validate()
        plot = Plot()
        self.list.append(plot)
        index = self.list.model().indexFromItem(plot)
        self.list.selectionModel().setCurrentIndex(index,
            QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        self.equation.setFocus()

    def plot_changed(self, selected, deselected):
        """Update the current plot attributes.
           Enable the input area if the selection is valid."""
        try:
            indices = selected.indexes()
        except:
            indices = []
        if len(indices) > 0:
            # We've selected a new plot.
            self.current_plot = indices[0]
            self.equation.setText(self.current_plot.data(ROLE_EQUATION))
            self.change_color_label(self.current_plot.data(ROLE_COLOR))
            self.input_frame.setEnabled(True)
        else:
            # We either deleted a plot or deselected one.
            self.current_plot = None
            self.equation.clear()
            self.reset_color_label()
            self.input_frame.setEnabled(False)
        self.validate()

    def equation_changed(self, text):
        """Called when the equation input is changed by the user.
           Starts the validation timer."""
        self.validation_indicator.setVisible(True)
        self.validation_timer.start(VALIDATION_DELAY)

    def validate(self):
        """Validates the input and changes the plot and the
           background of the input area accordingly."""
        self.validation_indicator.setVisible(False)
        self.validation_timer.stop()

        text = self.equation.text()
        color = QApplication.palette().color(QPalette.Base)
        if self.current_plot:
            plot = self.list.model().itemFromIndex(self.current_plot)
            if text != plot.data(ROLE_EQUATION):
                if not plot.set_equation(text):
                    color = QColor(250, 180, 180)
                else:
                    self.program.window.diagram.draw()

        palette = QPalette()
        palette.setColor(QPalette.Base, color)
        self.equation.setPalette(palette)
