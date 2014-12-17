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
    """A simple line in the form y = mx + c.
    
       The gradient stored is always between -1 and 1. Steep lines
       are stored by a flag that rotates the line 90 degrees.
       This is handy for avoiding infinite gradients. When rotated,
       the intercept stored is with the x axis.
       
       The flag is handled internally, and can be ignored when
       interfacing with the class."""
    def __init__(self, gradient, y_intercept=None, x_intercept=None):
        if -1 <= gradient <= 1:
            self.gradient = gradient
            self.intercept = y_intercept
            self.rotated = False
        else:
            self.gradient = -1 / gradient
            self.intercept = x_intercept
            self.rotated = True

    def y(self, x):
        """Calculate a y coordinate from an x coordinate."""
        return x * self.gradient + self.intercept

    def x(self, y):
        """Calculate an x coordinate from a y coordinate."""
        return (y - self.intercept) / self.gradient

    def collide(self, other):
        """Find the point where this and another line intercept.
           Return None if lines are parallel."""
        # Store the gradients and intercepts in temp variables.
        m0 = self.gradient
        m1 = other.gradient
        c0 = self.intercept
        c1 = other.intercept
        if m0 == m1:
            return None

        # Rotate everything 90 degrees if either line is vertical,
        # except when the other is horizontal.
        if m0 == float("inf"):
            if m1 == 0: pass  # TODO: something.
            m0 = 0
            m1 = -1 / m1
        elif m1 == float("inf"):
            if m0 == 0: pass  # TODO: something.
            m0 = -1 / m0
            m1 = 0

        # It doesn't matter which way round each individual
        # difference is, as long as the two are opposite.
        x = (c1 - c0) / (m0 - m1)
        return Point(x, self.y(x))


class Ray:
    def __init__(self, angle, origin):
        self.origin = origin
        self.angle = angle
