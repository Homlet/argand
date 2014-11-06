"""Argand Diagram Plotter

dialog_preferences.py - Creates a pop-up dialog for setting
                        diagram preferences.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class DialogPreferences(QDialog):
    def __init__(self, parent):
        super(DialogPreferences, self).__init__(parent)
        self.setup_content()
        self.initialize()
        
    def setup_content(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(3, 3, 3, 3)
        self.grid.setSizeConstraint(QLayout.SetFixedSize)
        
        # Create labels.
        self.stroke_label = QLabel("Stroke width:")
        self.font_size_label = QLabel("Font size:")
        
        # Create integer inputs.
        self.stroke = QSlider(Qt.Horizontal)
        self.stroke.setTickPosition(QSlider.TicksBelow)
        self.stroke.setRange(1, 10)
        self.stroke.setTickInterval(1)
        self.font_size = QSpinBox()
        
        # Create divider.
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.VLine)
        self.divider.setFrameShadow(QFrame.Sunken)
        
        # Create check-boxes.
        self.label_axes = QCheckBox("Label axes")
        self.label_points = QCheckBox("Label points")
        
        # Create Save and Cancel buttons.
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        # Add everything to the grid.
        self.grid.addWidget(self.stroke_label, 0, 0)
        self.grid.addWidget(self.stroke, 0, 1)
        self.grid.addWidget(self.font_size_label, 1, 0)
        self.grid.addWidget(self.font_size, 1, 1)
        self.grid.addWidget(self.divider, 0, 2, 2, 1)
        self.grid.addWidget(self.label_axes, 0, 3)
        self.grid.addWidget(self.label_points, 1, 3)
        self.grid.addWidget(self.buttons, 2, 0, 1, 4, Qt.AlignRight)
    
    def initialize(self):
        self.setWindowTitle("Preferences")
