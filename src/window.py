"""Argand Diagram Plotter

window.py - Creates the main window of the program.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import log10
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from dialog_plots import DialogPlots
from dialog_preferences import DialogPreferences
from preferences import Preferences
from view_diagram import ViewDiagram
from geometry import Point


class Window(QMainWindow):
    def __init__(self, program):
        super(Window, self).__init__()
        self.program = program
        self.setup_content()
        self.create_actions()
        self.setup_menubar()
        self.initialize()

    def setup_content(self):
        # Setup a central container widget.
        self.center = QWidget()
        self.setCentralWidget(self.center)

        # Add a graphics area for drawing the diagram.
        self.diagram = ViewDiagram(self.program)

        # Create a control region under the diagram.
        self.translation_label = QLabel()
        self.translation_label.setPixmap(QPixmap(
            self.program.get_path("img/position16.png")))

        self.translation_input_x = QLineEdit("0")
        self.translation_input_x.setFixedWidth(53)
        self.translation_input_x.setAlignment(Qt.AlignRight)
        self.translation_input_x.setValidator(QDoubleValidator(decimals=4))
        self.translation_input_x.textChanged.connect(self.input_to_translation)

        self.translation_input_y = QLineEdit("0")
        self.translation_input_y.setFixedWidth(53)
        self.translation_input_y.setAlignment(Qt.AlignRight)
        self.translation_input_y.setValidator(QDoubleValidator(decimals=4))
        self.translation_input_y.textChanged.connect(self.input_to_translation)

        self.zoom_label = QLabel()
        self.zoom_label.setPixmap(QPixmap(
            self.program.get_path("img/zoom16.png")))

        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setFixedWidth(150)
        self.zoom_slider.setRange(-50, 100)
        self.zoom_slider.valueChanged.connect(self.slider_to_zoom)

        # Create a grid layout in the central widget.
        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 1)
        self.grid.setContentsMargins(1, 1, 1, 1)
        self.grid.setSpacing(2)
        self.center.setLayout(self.grid)

        # Add everything to the grid.
        self.grid.addWidget(self.diagram, 0, 0, 1, 0)
        self.grid.addWidget(self.translation_label, 1, 1)
        self.grid.addWidget(self.translation_input_x, 1, 2)
        self.grid.addWidget(self.translation_input_y, 1, 3)
        self.grid.addItem(QSpacerItem(8, 0), 1, 4)
        self.grid.addWidget(self.zoom_label, 1, 5)
        self.grid.addWidget(self.zoom_slider, 1, 6)

        # Add the plot list docking dialog.
        self.plots = DialogPlots(self, self.program)
        self.plots.list.deleted_item.connect(self.diagram.draw)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.plots)

        # Create an about dialog for the program.
        self.about = QMessageBox()

    def create_actions(self):
        self.a_new = QAction("&New", self)
        self.a_new.setShortcut("Ctrl+N")
        self.a_new.triggered.connect(self.program.new_diagram)

        self.a_open = QAction("&Open", self)
        self.a_open.setShortcut("Ctrl+O")
        self.a_open.triggered.connect(self.program.open_diagram)

        self.a_save = QAction("&Save", self)
        self.a_save.setShortcut("Ctrl+S")
        self.a_save.triggered.connect(self.program.save_diagram)

        self.a_save_as = QAction("Save &As...", self)
        self.a_save_as.setShortcut("Ctrl+Shift+S")
        self.a_save_as.triggered.connect(self.program.save_diagram_as)

        self.a_exit = QAction("&Exit", self)
        self.a_exit.setShortcut("Ctrl+W")
        self.a_exit.triggered.connect(qApp.quit)

        self.a_reset_view = QAction("&Reset View", self)
        self.a_reset_view.setShortcut("Ctrl+R")
        self.a_reset_view.triggered.connect(self.reset_translation)
        self.a_reset_view.triggered.connect(self.reset_zoom)

        self.a_toggle_plots = self.plots.toggleViewAction()
        self.a_toggle_plots.setShortcut("Ctrl+P")

        self.a_show_prefs = QAction("&Preferences...", self)
        self.a_show_prefs.setShortcut("Ctrl+,")
        self.a_show_prefs.triggered.connect(self.show_preferences)

        self.a_show_about = QAction("&About Argand Plotter", self)
        self.a_show_about.triggered.connect(self.show_about)
        self.a_show_about_qt = QAction("About &Qt", self)
        self.a_show_about_qt.triggered.connect(qApp.aboutQt)

    def setup_menubar(self):
        menubar = self.menuBar()

        menu_file = menubar.addMenu("&File")
        menu_file.addAction(self.a_new)
        menu_file.addAction(self.a_open)
        menu_file.addAction(self.a_save)
        menu_file.addAction(self.a_save_as)
        menu_file.addSeparator()
        menu_file.addAction(self.a_exit)

        menu_view = menubar.addMenu("&View")
        menu_view.addAction(self.a_reset_view)
        menu_view.addSeparator()
        menu_view.addAction(self.a_toggle_plots)
        menu_view.addAction(self.a_show_prefs)

        menu_help = menubar.addMenu("&Help")
        #menu_help.addAction(self.a_show_docs)
        menu_help.addSeparator()
        menu_help.addAction(self.a_show_about)
        menu_help.addAction(self.a_show_about_qt)

    def initialize(self):
        self.setGeometry(200, 150, 800, 600)
        self.setWindowTitle("Argand Diagram Plotter")

        self.program.diagram_changed.connect(self.register_signals)
        self.program.diagram_changed.connect(self.set_title)

        self.show()

    def set_title(self):
        """Put the name of the current diagram file in the title bar."""
        if hasattr(self.program, "diagram") and self.program.diagram:
            self.setWindowTitle(
                "Argand Plotter - " + self.program.diagram.filename)
        else:
            self.setWindowTitle("Argand Plotter")

    def register_signals(self):
        """Register all external PyQt signal connections."""
        self.program.diagram.translation_changed.connect(
            self.translation_to_input)
        self.program.diagram.zoom_changed.connect(self.zoom_to_slider)

    def show_preferences(self):
        DialogPreferences(self, self.program.preferences).exec_()
        self.diagram.draw()

    def show_about(self):
        QMessageBox.about(self, "About Argand Plotter",
            "Argand Plotter is a program for drawing Argand Diagrams.\n\n"
            "The program was written by Sam Hubbard, as a project for his "
            "A2 computing coursework.\n\n"
            "Copyright (C) 2015 Sam Hubbard")

    def input_to_translation(self):
        """Set the translation in the diagram, from the inputs."""
        self.program.diagram.set_translation(Point(
            float(self.translation_input_x.text()),
            float(self.translation_input_y.text())), False)
        self.diagram.draw()

    def translation_to_input(self, value):
        """Set the values of the translation inputs."""
        self.translation_input_x.setText(str(round(value.x, 4)))
        self.translation_input_y.setText(str(round(value.y, 4)))

    def reset_translation(self):
        """Reset the translation to the origin."""
        self.program.diagram.set_translation(Point(0, 0))
        self.diagram.draw()
    
    def slider_to_zoom(self):
        """Set the zoom in the diagram, from the slider."""
        self.program.diagram.set_zoom(
            10 ** (self.zoom_slider.value() / 25), False)
        self.diagram.draw()

    def zoom_to_slider(self, value):
        """Set the value of the zoom slider."""
        if -50 <= 25 * log10(value) <= 100:
            self.zoom_slider.setValue(25 * log10(value))

    def reset_zoom(self):
        """Reset zoom level to 1."""
        self.program.diagram.set_zoom(1)
        self.diagram.draw()
