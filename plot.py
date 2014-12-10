"""Argand Diagram Plotter

plot.py - Class for storing a single drawable plot.

Written by Sam Hubbard - samlhub@gmail.com
"""

from functools import reduce

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from geometry import *
from abstract_syntax_tree import *


TYPE_CIRCLE = 0
TYPE_DISK = 1
TYPE_NEGATIVE_DISK = 2

TYPE_LINE = 3
TYPE_HALF_PLANE = 4

TYPE_RAY = 5
TYPE_SECTOR = 6

ROLE_EQUATION = Qt.UserRole
ROLE_TYPE = Qt.UserRole + 1
ROLE_SHAPE = Qt.UserRole + 2
ROLE_COLOR = Qt.UserRole + 10
ROLE_BUTTON_STATE = Qt.UserRole + 11

STATE_NORMAL = 0
STATE_HOVER = 1
STATE_DOWN = 2


class Plot(QStandardItem):
    def __init__(self, equation="", color=QColor(0, 0, 0)):
        super(Plot, self).__init__()

        self.set_equation(equation)
        self.setData(color, ROLE_COLOR)

    def set_equation(self, equation):
        tree = SyntaxParser(equation).get_tree()
        if tree and self.classify(tree):
            self.setData(equation, ROLE_EQUATION)
            return True
        return False

    def classify(self, tree):
        """Attempt to classify the AST as a particular type
           Argand diagram. Returns true if successful."""
        def values(node):
            """Calculates coefficients and offsets for each node.
               Returns a tuple: (coefficient, offset)."""
            if node.type == NODE_TYPE_VAR:
                return (1, 0)
            if node.type == NODE_TYPE_NUM:
                return (0, node.value)
            if node.type == NODE_TYPE_OP:
                if len(node.children) == 2:
                    if node.value == CODE["add"]:
                        # Annoyingly, we have to create a and b inside each
                        # case to avoid wasting processing on recursion.
                        a = values(node.children[0])
                        b = values(node.children[1])
                        return (a[0] + b[0], a[1] + b[1])
                    if node.value == CODE["sub"]:
                        a = values(node.children[0])
                        b = values(node.children[1])
                        return (a[0] - b[0], a[1] - b[1])
                    if node.value == CODE["mul"]:
                        a = values(node.children[0])
                        b = values(node.children[1])
                        # Only one child of a mul node may have a variable.
                        if (a[0] ^ b[0]) and a[0]:
                            return (a[0] * b[1], a[1] * b[1])
                        if (a[0] ^ b[0]) and b[0]:
                            return (a[1] * b[0], a[1] * b[1])
                    if node.value == CODE["div"]:
                        a = values(node.children[0])
                        b = values(node.children[1])
                        # Only the left child of a div node may have a var.
                        if b[0] == 0:
                            return (a[0] / b[1], a[1] / b[1])
                
                # This node doesn't support variable children (unless
                # it is a root node, but we've already accounted for those).
                # Just evaluate it numerically, and treat as an offset.
                return (0, node.resolve())
        
        def inspect(left, right):
            """Attempts to classify the equation based
               on its two halves. Call with the halves
               switched to account for all possibilities."""
            # Handle all the cases!
            if left.value == CODE["mod"]:
                left_values = values(left.children[0])
                if right.value == CODE["mod"]:
                    # We have a perpendicular bisector (line).
                    pass
                else:
                    # We have a circle (hopefully).
                    right_values = values(right)
                    if left_values[0] == 1 and right_values[0] == 0:
                        center = Point(
                            -left_values[1].real,
                            -left_values[1].imag)
                        radius = right_values[1].real
                        self.setData(TYPE_CIRCLE, ROLE_TYPE)
                        self.setData(Circle(center, radius), ROLE_SHAPE)
                        return True
            return False
        
        # If the code throws an error, the input is probably wrong.
        try:
            # Get the right and left halves of the equation.
            left = tree.children[0]
            right = tree.children[1]
            if inspect(left, right): return True
            if inspect(right, left): return True
        except Exception as e:
            print(e)
        return False
