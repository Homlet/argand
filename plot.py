"""Argand Diagram Plotter

plot.py - Class for storing a single drawable plot.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import pi, atan2

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

REL_LESS = "LESS"
REL_LEQL = "LEQL"
REL_EQL = "EQL"
REL_MEQL = "MEQL"
REL_MORE = "MORE"

def invert_relation(relation):
    if relation == REL_MORE: return REL_LESS
    if relation == REL_MEQL: return REL_LEQL
    if relation == REL_EQL: return REL_EQL
    if relation == REL_LEQL: return REL_MEQL
    if relation == REL_LESS: return REL_MORE

ROLE_EQUATION = Qt.UserRole
ROLE_TYPE = Qt.UserRole + 1
ROLE_RELATION = Qt.UserRole + 2
ROLE_SHAPE = Qt.UserRole + 3
ROLE_COLOR = Qt.UserRole + 10
ROLE_BUTTON_STATE = Qt.UserRole + 11

STATE_NORMAL = 0
STATE_HOVER = 1
STATE_DOWN = 2


class Plot(QStandardItem):
    def __init__(self, equation="", color=QColor(0, 0, 0, 80)):
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
                # All variables have coefficient 1.
                return (1, 0)
            if node.type == NODE_TYPE_NUM:
                # All numbers represent an offset of their value.
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
                        if (bool(a[0]) ^ bool(b[0])) and bool(a[0]):
                            return (a[0] * b[1], a[1] * b[1])
                        if (bool(a[0]) ^ bool(b[0])) and bool(b[0]):
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
        
        def inspect(left, right, relation="EQL"):
            """Attempts to classify the equation based
               on its two halves. Call with the halves' order
               switched to account for all possibilities."""
            # Handle all the cases!
            if left.value == CODE["mod"]:
                left_values = values(left.children[0])
                if right.value == CODE["mod"]:
                    right_values = values(right.children[0])
                    if left_values[0] == 1 and right_values[0] == 1:
                        if relation == REL_EQL:
                            # We have a perpendicular bisector (line).
                            type = TYPE_LINE
                        else:
                            # We have a half plane.
                            type = TYPE_HALF_PLANE
                        # p0 and p1 are the points to bisect.
                        p0 = Point(
                            -left_values[1].real,
                            -left_values[1].imag)
                        p1 = Point(
                            -right_values[1].real,
                            -right_values[1].imag)
                        center = Point((p0.x + p1.x) / 2, (p0.y + p1.y) / 2)
                        # The gradient of the bisector is -1/m.
                        try:
                            gradient = -(p1.x - p0.x) / (p1.y - p0.y)
                            intercept = center.y - gradient * center.x
                            if type == TYPE_HALF_PLANE:
                                above = ((relation in [REL_MORE, REL_MEQL])
                                       ^ (p0.y > p1.y))
                        except:
                            # If a division by zero occurred, the bisector
                            # must be vertical.
                            gradient = float("inf")
                            intercept = center.x
                        self.setData(type, ROLE_TYPE)
                        self.setData(relation, ROLE_RELATION)
                        if type == TYPE_LINE:
                            self.setData(Line(gradient, intercept), ROLE_SHAPE)
                        else:
                            self.setData(HalfPlane(gradient, intercept, above),
                                ROLE_SHAPE)
                        return True
                else:
                    right_values = values(right)
                    if right_values[0] == 0:
                        if relation == REL_EQL:
                            # We have a circle.
                            type = TYPE_CIRCLE
                        elif relation in [REL_LEQL, REL_LESS]:
                            # We have a disk.
                            type = TYPE_DISK
                        else:
                            # We have a negative disk.
                            type = TYPE_NEGATIVE_DISK
                            # Negative disks not supported yet.
                            return False
                        center = Point(
                            -left_values[1].real / left_values[0].real,
                            -left_values[1].imag / left_values[0].real)
                        radius = right_values[1].real / abs(left_values[0])
                        self.setData(type, ROLE_TYPE)
                        self.setData(relation, ROLE_RELATION)
                        self.setData(Circle(center, radius), ROLE_SHAPE)
                        return True
            if left.value == CODE["ARG"]:
                left_values = values(left.children[0])
                right_values = values(right)
                if relation == REL_EQL:
                    # We have a ray.
                    type = TYPE_RAY
                else:
                    # We have a sector.
                    type = TYPE_SECTOR
                    # Sectors are not supported yet.
                    return False
                if left_values[0] != 1:
                    # Coefficients aren't supported here.
                    return False
                endpoint = Point(
                    -left_values[1].real,
                    -left_values[1].imag)
                angle = right_values[1].real % (2 * pi)
                self.setData(type, ROLE_TYPE)
                self.setData(relation, ROLE_RELATION)
                self.setData(Ray(angle, endpoint), ROLE_SHAPE)
                return True
            return False
        
        # If the code throws an error, the input is probably wrong.
        # TODO: tool-tips.
        try:
            # Get the relation from the root node,
            # which is probably a relation node.
            for operator, function in CODE.items():
                if tree.value == function:
                    relation = operator
            # Get the right and left halves of the equation.
            left = tree.children[0]
            right = tree.children[1]
            # inspect() will fill out the data if successful.
            if inspect(left, right, relation): return True
            # Try the equation the other way round.
            if inspect(right, left, invert_relation(relation)): return True
        except Exception as e:
            print(e)
        return False
