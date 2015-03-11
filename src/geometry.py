"""Implementation of various maths classes.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import pi, tan, atan2, cos, sin


ABOVE = 0x01
RIGHT = 0x10


class Point:
    """Stores a 2 dimensional vector (point).
    
    Attributes:
        x: The x coordinate of the point.
        y: The y coordinate of the point.
    """
    KEY_ERROR_MSG = "Invalid key for two-dimensional point."

    def __init__(self, x=0.0, y=0.0, c=None):
        """Create a new point.

        Create a point using x and y coordinates. If a complex
        number is supplied as c, x and y are ignored and the complex
        number is used to create the point.
        
        Args:
            x: The x coordinate of the point.
            y: The y coordinate of the point.
            c: Optional complex number representing the point.
        """
        if c != None:
            self.x = c.real
            self.y = c.imag
        else:
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
    """Stores a circle by center and radius.
    
    Attributes:
        center: A point describing the center of the circle.
        radius: The radius of the circle.
    """
    def __init__(self, center, radius):
        """Create a new circle.

        Args:
            center: A point describing the center of the circle.
            radius: The radius of the circle.
        """
        self.center = center
        self.radius = radius

    def origin(self):
        """Calculate the bottom left corner of the circle.

        Returns:
            A point representing the bottom left corner of the axis-aligned
            square that bounds the circle.
        """
        return Point(self.center.x - self.radius, self.center.y - self.radius)

    def diameter(self):
        """Calculate the diameter from the radius.

        Returns:
            The diameter (twice the radius).
        """
        return 2 * self.radius

    def point(self, theta):
        """Calculate a point on the circle.

        Args:
            theta: The angle to rotate from the positive x-axis.

        Returns:
            A point on the circle found by rotating theta radians
            anti-clockwise from the positive x-axis.
        """
        return self.center + Point(cos(theta), sin(theta)) * self.radius


class Line:
    """Stores line by gradient and intercept.

    The intercept stored is with the y-axis for all real gradients.
    For complex gradients, the intercept is with the x-axis.

    Attributes:
        gradient: The gradient of the line (rise / run).
        intercept: The intercept of the line with the y (or x) axis.
    """
    def __init__(self, gradient, intercept):
        """Create a new line.
        
        Args:
            gradient: The gradient of the line (rise / run).
            intercept: The intercept of the line with the y (or x) axis.
        """
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
        
        Return:
            The point at which the lines cross, or None if the
            lines are parallel.
        """
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


class HalfPlane(Line):
    """Stores a half plane as a line and a side.

    Attributes:
        side: The side of the line contained in the plane.
    """
    def __init__(self, gradient, intercept, side):
        super(HalfPlane, self).__init__(gradient, intercept)
        self.side = side

    def __contains__(self, point):
        error = point.y - self.gradient * point.x - self.intercept * self.side
        return error >= 0


class Ray:
    """Store a ray projected from a point at an angle.
    
    A ray is an infinitely long line with a single endpoint.
    
    Attributes:
        angle: The angle at which to project the ray.
        endpoint: The point to project the ray from.
    """
    def __init__(self, angle, endpoint):
        self.angle = angle % (2 * pi)
        self.endpoint = endpoint

    def intersect(self, line):
        """Intersect this ray with a line.
        
        Return:
            The point at which the ray crosses the line, or None if no
            intersection found.
        """
        # Create a temporary line representing this ray.
        m = tan(self.angle)
        c = self.endpoint.y - self.endpoint.x * m
        l = Line(m, c)

        # Find the intersection between this line and the argument.
        p = l.intersect(line)

        # Make sure the point is on the correct side of the ray's endpoint.
        if 0 < self.angle < pi and p.y > self.endpoint.y      \
        or pi < self.angle < 2 * pi and p.y < self.endpoint.y \
        or self.angle == 0 and p.x > self.endpoint.x          \
        or self.angle == pi and p.x < self.endpoint.x:
            return p
        else:
            return None

class DualRay:
    """Stores two opposite rays.
    
    Given two endpoints, find the rays from these points facing away
    from each other.
    
    Attributes:
        rays: List containing the rays.
    """
    def __init__(self, endpoints):
        angle = atan2(endpoints[1].y - endpoints[0].y,
                      endpoints[1].x - endpoints[0].x)
        self.rays = (Ray(angle, endpoints[1]), Ray(angle + pi, endpoints[0]))


def project(point, offset, zoom):
    return (point - offset) * zoom


def unproject(point, offset, zoom):
    return (point / zoom) + offset
