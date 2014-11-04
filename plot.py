"""Argand Diagram Plotter

Written by Sam Hubbard - samlhub@gmail.com
"""

from abstract_syntax_tree import SyntaxParser


TYPE_CIRCLE = 0
TYPE_DISK = 1
TYPE_NEGATIVE_DISK = 2

TYPE_LINE = 3
TYPE_HALF_PLANE = 4

TYPE_RAY = 5
TYPE_SECTOR = 6


class Plot:
    def __init__(self, equation, color=0, alpha=0.0):
        self.equation = equation
        self.color = color
        self.alpha = alpha
        
        self.parser = SyntaxParser(self.equation)
        self.parser.parse()


if __name__ == "__main__":
    plot = Plot(input())
    if plot.parser.parsed:
        print(plot.parser.resolve())
