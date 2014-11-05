"""Argand Diagram Plotter

dialog_preferences.py - Creates a pop-up dialog for setting
                        diagram preferences.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class DialogPreferences(QDialog):
    def __init__(self, parent):
        super(DialogPreferences, self).__init__(parent, Qt.Tool)
        self.setup_content()
        self.initialize()
        
    def setup_content(self):
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(3, 3, 3, 3)
        
        # Create Save and Cancel buttons.
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        # Add everything to the grid.
        self.grid.addWidget(self.buttons)
    
    def initialize(self):
        self.setWindowTitle("Preferences")
