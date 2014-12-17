"""Argand Diagram Plotter

geometry.py - Impletements vector maths types.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import pi, tan


class Point:
    KEY_ERROR_MSG = "Invalid key for two-dimensional point."
    
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other[0], -other[1])

    def __mul__(self, other):
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        else:
            return Point(self.x * other, self.y * other)

    def __div__(self, other):
        return Point(self.x / other, self.y / other)

    def __len__(self):
        return 2

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __repr__(self):
        return "Point" + repr((self.x, self.y))

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise KeyError(KEY_ERROR_MSG)

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        if index == 1:
            self.y = value
        raise KeyError(KEY_ERROR_MSG)

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def origin(self):
        return Point(self.center.x - self.radius, self.center.y - self.radius)
    
    def diameter(self):
        return 2 * self.radius

class Line:
    def __init__(self, point, angle):
        self.point = point
        self.angle = angle
        self.gradient = tan(angle)

    def entry(self, rect):
        """Returns the point at which the line enters a rectangle.
           If the line does not intersect, return None."""
        pass

class Ray:
    def __init__(self, angle, origin):
        self.origin = origin
        self.angle = angle
