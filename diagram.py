"""Argand Diagram Plotter

diagram.py - Stores all information pertaining to
             a single instance of a diagram.

Written by Sam Hubbard - samlhub@gmail.com
"""

from geometry import Point


class Diagram:
    def __init__(self):
        self.plots = []
        self.zoom = 1.0
        self.translation = Point(0.0, 0.0)

    def add_plot(self, plot, index):
        pass
    
    def remove_plot(self, index):
        pass

    def get_plot(self, index):
        pass

    def set_zoom(self, zoom):
        self.zoom = zoom

    def set_translation(self, translation):
        self.translation = translation

    def translate(self, translation):
        self.translation += translation
