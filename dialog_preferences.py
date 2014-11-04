"""Argand Diagram Plotter

dialog_preferences.py - Creates a pop-up dialog for setting
                        diagram preferences.

Written by Sam Hubbard - samlhub@gmail.com
"""

from PyQt4 import QtGui, QtCore


class DialogPreferences(QtGui.QDialog):
	def __init__(self, parent):
        super(DialogPreferences, self).__init__("Preferences", parent)
        self.setup_content()
        self.initialize()
		
	def setup_content(self):
		self.grid = QGui.QGridLayout(self)
		self.grid.setContentMargins(3, 3, 3, 3)
	
	def initialize(self):
		pass
