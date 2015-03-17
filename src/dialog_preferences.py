"""Preferences Dialog

Implementation of a pop-up dialog for setting
program preferences.

Written by Sam Hubbard - samlhub@gmail.com
Copyright (C) 2015 Sam Hubbard
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class DialogPreferences(QDialog):
    def __init__(self, parent, preferences):
        super(DialogPreferences, self).__init__(
            parent, Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        )
        self.preferences = preferences
        self.setup_content()
        self.initialize()

    def setup_content(self):        
        # Create labels.
        self.stroke_label = QLabel("Stroke width:")
        #self.font_size_label = QLabel("Font size:")

        # Create integer inputs.
        self.stroke = QSpinBox()
        self.stroke.setRange(1, 10)
        self.stroke.setValue(self.preferences.stroke)
        #self.font_size = QSpinBox()
        #self.font_size.setRange(12, 24)
        #self.font_size.setValue(self.preferences.font_size)

        # Create divider.
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.VLine)

        # Create check-boxes.
        self.label_axes = QCheckBox("Label axes")
        self.label_axes.setChecked(self.preferences.label_axes)
        self.label_points = QCheckBox("Label points")
        self.label_points.setChecked(self.preferences.label_points)

        # Create Save and Cancel buttons.
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Create a grid layout in the widget.
        grid = QGridLayout()
        grid.setContentsMargins(3, 3, 3, 3)
        grid.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(grid)

        # Add everything to the grid.
        grid.addWidget(self.stroke_label, 0, 0)
        grid.addWidget(self.stroke, 0, 1)
        #grid.addWidget(self.font_size_label, 1, 0)
        #grid.addWidget(self.font_size, 1, 1)
        grid.addWidget(self.divider, 0, 2, 2, 1)
        grid.addWidget(self.label_axes, 0, 3)
        grid.addWidget(self.label_points, 1, 3)
        grid.addWidget(self.buttons, 2, 0, 1, 4, Qt.AlignRight)

    def initialize(self):
        self.setWindowTitle("Preferences")

    def accept(self, *args, **kwargs):
        self.preferences.stroke = self.stroke.value()
        #self.preferences.font_size = self.font_size.value()
        self.preferences.label_axes = self.label_axes.isChecked()
        self.preferences.label_points = self.label_points.isChecked()
        super(DialogPreferences, self).accept(*args, **kwargs)
