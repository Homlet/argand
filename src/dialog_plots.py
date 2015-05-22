"""Plots Dialog

Dockable dialog for creating and managing plots.

Written by Sam Hubbard - samlhub@gmail.com
Copyright (C) 2015 Sam Hubbard
"""

from time import time

from PySide.QtGui import *
from PySide.QtCore import *

from plot import *
from plot_list import *
from abstract_syntax_tree import SyntaxParser


class DialogPlots(QDockWidget):
    """A dockable dialog that displays the list of plots in the diagram.
    
    Attributes:
        program: A reference to the program object.
    """
    def __init__(self, parent, program):
        """Create the dialog.
        
        Args:
            parent: Reference to the parent window (main window).
            program: See DialogPlots.program.
        """
        super(DialogPlots, self).__init__("Plots", parent)
        self.program = program
        self.current_plot = None

        self.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setup_content()

    def setup_content(self):
        """Add the widgets and layouts to the dialog."""
        # Setup the container widget.
        self.widget = QWidget()
        self.widget.setMinimumSize(200, 300)

        # Setup the list of plots.
        self.list = PlotListTable()

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
        color_button_pixmap = QPixmap(
            self.program.get_path("img/color16.png"))
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
        
        self.setWidget(self.widget)

    @Slot()
    def initialize(self):
        """Register signals once the event loop is running."""
        self.register_signals()
        
        self.show()

    def register_signals(self):
        """Register all external PyQt signal connections."""
        self.program.diagram_changed.connect(self.set_list_model)
        self.list.deleted_item.connect(self.program.window.diagram.draw)

    def set_list_model(self):
        """Set the model the list will display plots from."""
        self.list.setModel(self.program.diagram.plots)
        # We have to store this in a variable to get around GC weirdness.
        selection_model = self.list.selectionModel()
        selection_model.selectionChanged.connect(self.plot_changed)
        self.list.resize_headers()
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
        """Change the color of the label in the input area.
        
        Args:
            color: The new color of the label."""
        color = QColor(color.rgb())
        self.color_label.setPalette(QPalette(color))
        self.color_label.setAutoFillBackground(True)

    def reset_color_label(self):
        """Set the color label to transparent."""
        self.color_label.setAutoFillBackground(False)

    @Slot()
    def add_plot(self):
        """Add a new plot to the plot list and select it."""
        self.validate()
        plot = Plot()
        self.list.append(plot)
        index = self.list.model().indexFromItem(plot)
        self.list.selectionModel().setCurrentIndex(index,
            QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        self.equation.setFocus()

    @Slot(QItemSelection, QItemSelection)
    def plot_changed(self, selected, deselected):
        """Update the current plot attributes.
        
        This will enable the input area if the selection is valid.
        
        Args:
            selected: List of newly selected entries.
            deselected: List of newly deselected entries.
        """
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

    @Slot(str)
    def equation_changed(self, text):
        """Called when the equation input is changed by the user.
        
        Validate the input.
        
        Args:
            text: The updated content of the equation input.
        """
        self.validate()

    @Slot()
    def validate(self):
        """Validates the equation input.
        
        Also changes the plot and the background of the
        input area accordingly.
        """
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
