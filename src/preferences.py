"""Preferences

Object for storing program preferences.

Written by Sam Hubbard - samlhub@gmail.com
Copyright (C) 2015 Sam Hubbard
"""

DEFAULT_STROKE = 1
#DEFAULT_FONT_SIZE = 12  # Some day...
DEFAULT_LABEL_AXES = True
DEFAULT_LABEL_POINTS = False


class Preferences:
    """Simple class to store program preferences.

    Attributes:
        stroke: The width in pixels of lines on the diagram.
        label_axes: Whether labels should be drawn on the axes.
        label_points: Whether points should be labelled on the diagram.
    """

    def __init__(self):
        """Construct the object with default attributes."""
        self.stroke = DEFAULT_STROKE
        #self.font_size = DEFAULT_FONT_SIZE
        self.label_axes = DEFAULT_LABEL_AXES
        self.label_points = DEFAULT_LABEL_POINTS
