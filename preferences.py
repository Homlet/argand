"""Argand Diagram Plotter

preferences.py - Object for storing program preferences.

Written by Sam Hubbard - samlhub@gmail.com
"""

DEFAULT_STROKE = 1
#DEFAULT_FONT_SIZE = 12  # Some day...
DEFAULT_LABEL_AXES = True
DEFAULT_LABEL_POINTS = False


class Preferences:
    def __init__(self):
        self.stroke = DEFAULT_STROKE
        #self.font_size = DEFAULT_FONT_SIZE
        self.label_axes = DEFAULT_LABEL_AXES
        self.label_points = DEFAULT_LABEL_POINTS
