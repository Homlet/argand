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
        def get_variables(tree):
            """Returns a list of variable node references,
               sorted by depth (deepest first)."""
            queue = [tree]
            variables = []
            while queue:
                node = queue.pop(0)
                if node.type == NODE_TYPE_VAR:
                    variables.insert(0, node)
                queue.extend(node.children)
            return variables
        def values(node):
            """Calculates coefficients and offsets for each node.
               Returns a tuple: (coefficient, offset)."""
            if node.type == NODE_TYPE_VAR:
                return (1, 0)
            if node.type == NODE_TYPE_NUM:
                return (0, node.value)
            if node.type == NODE_TYPE_OP:
                # TODO: validation here.
                a = values(node.children[0])
                b = values(node.children[1])
                if node.value == CODE["add"]:
                    return (a[0] + b[0], a[1] + b[1])
                if node.value == CODE["sub"]:
                    return (a[0] - b[0], a[1] - b[1])
                if node.value == CODE["mul"]:
                    if a[0]:
                        return (a[0] * b[1], a[1] * b[1])
                    else:
                        return (a[1] * b[0], a[1] * b[1])
                if node.value == CODE["div"]:
                    return (a[0] / b[1], a[1] / b[1])
                return (0, node.resolve())
        
        print(values(tree.children[0]))
        return False

def vals(dictionary, keys):
    return [dictionary[key] for key in keys]
