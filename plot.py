"""Argand Diagram Plotter

plot.py - Class for storing a single drawable plot.

Written by Sam Hubbard - samlhub@gmail.com
"""

from functools import reduce

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from abstract_syntax_tree import *


TYPE_CIRCLE = 0
TYPE_DISK = 1
TYPE_NEGATIVE_DISK = 2

TYPE_LINE = 3
TYPE_HALF_PLANE = 4

TYPE_RAY = 5
TYPE_SECTOR = 6

ROLE_EQUATION = Qt.UserRole
ROLE_TREE = Qt.UserRole + 1
ROLE_COLOR = Qt.UserRole + 2
ROLE_BUTTON_STATE = Qt.UserRole + 3

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
            self.setData(tree, ROLE_TREE)
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
        
        # Get the right and left halves of the equation.
        left = tree.children[0]
        right = tree.children[1]
        print(values(left), values(right))
        return False
