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
    """A simple line in the form y = mx + c."""
    def __init__(self, gradient, intercept):
        self.gradient = gradient
        # Note: Iff the line is vertical, the intercept is
        #       assumed to be with the x-axis.
        self.intercept = intercept

    def y(self, x):
        """Calculate a y coordinate from an x coordinate."""
        return x * self.gradient + self.intercept

    def x(self, y):
        """Calculate an x coordinate from a y coordinate."""
        # This will throw an error if line is horizontal.
        return (y - self.intercept) / self.gradient

    def intersect(self, other):
        """Find the point where this and another line intersect.
           Return None if lines are parallel."""
        # Store the gradients and intercepts in temp variables.
        m0 = self.gradient
        m1 = other.gradient
        c0 = self.intercept
        c1 = other.intercept
        
        # If the gradients are the same, the lines are parallel.
        # Parallel lines never intersect at one point.
        if m0 == m1:
            return None

        if m0 == float("inf"):
            return Point(self.intercept, other.y(self.intercept))
        if m1 == float("inf"):
            return Point(other.intercept, self.y(other.intercept))

        # It doesn't matter which way round each individual
        # difference is, as long as the two are opposite.
        x = (c1 - c0) / (m0 - m1)
        return Point(x, self.y(x))


class Ray:
    def __init__(self, angle, endpoint):
        self.angle = angle
        self.endpoint = endpoint

    def intersect(self, line):
        """Intersect this ray with a line.
           Return None if no intersection found."""
        # Create a temporary line representing this ray.
        m = tan(self.angle)
        c = self.endpoint.y - self.endpoint.x * m
        l = Line(m, c)
        
        # Find the intersection between this line and the argument.
        p = l.intersect(line)
        
        # Make sure the point is on the correct side of the ray's endpoint.
        return p