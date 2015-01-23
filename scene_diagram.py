"""Argand Diagram Plotter

scene_diagram.py - Implements QGraphicsScene for
                   drawing plots axes and labels
                   in the drawing area.

Written by Sam Hubbard - samlhub@gmail.com
"""

from math import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from plot import *
from geometry import *
from utils import clamp, floor_to


CLING_THRES = 10
LABEL_PAD = 20
TICK_SIZE = 2


class FlippedText(QGraphicsTextItem):
    """A vertically flipped text item.

    This is needed for using a properly oriented Cartesian
    coordinate system with QGraphicsScene, unfortunately.
    """
    def __init__(self, text, x, y):
        super(FlippedText, self).__init__()
        self.setPos(x, y)
        self.setPlainText(text)
        h_width = self.boundingRect().width() / 2
        h_height = self.boundingRect().height() / 2
        transform = QTransform()
        transform.translate(h_width, h_height)
        transform.scale(1, -1)
        transform.translate(-h_width, -h_height)
        self.setTransform(transform)


class SceneDiagram(QGraphicsScene):
    """Implementation of QGraphicsScene for drawing diagrams."""
    def __init__(self, program):
        super(SceneDiagram, self).__init__()
        self.program = program
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

    def draw_axes(self):
        """Draws the real and imaginary axes.

        If the current preferences allow it, the axes will
        be labelled. Labels will expand as the zoom increases.

        If the axes are too far from the viewport, they will
        'cling' to the edges of the screen, but the labels
        will still change.
        """
        width = self.sceneRect().width()
        height = self.sceneRect().height()

        translation = self.program.diagram.translation
        zoom = self.program.diagram.zoom
        origin = -translation * zoom

        # Clamp coordinates so the axes cling to the edge of the screen.
        cling_x = clamp(
            origin.x,
            CLING_THRES - width / 2,
            width / 2 - CLING_THRES
        )
        cling_y = clamp(
            origin.y,
            CLING_THRES - height / 2,
            height / 2 - CLING_THRES
        )

        # Draw the axes.
        self.addLine(width / 2 + cling_x, 0, width / 2 + cling_x, height)
        self.addLine(0, height / 2 + cling_y, width, height / 2 + cling_y)

        # If enabled, label the axes.
        if self.program.preferences.label_axes:
            # Draw the Re and Im labels.
            self.addItem(FlippedText(
                "Re",
                width - LABEL_PAD,
                height / 2 + cling_y - 2 * CLING_THRES
            ))
            self.addItem(FlippedText(
                "Im",
                width / 2 + cling_x - 2 * CLING_THRES,
                height - LABEL_PAD
            ))

            # Set the step using the order of magnitude of the current zoom.
            step = 10 ** floor_to(2 - log10(zoom), log10(5))
            pixels = step * zoom

            re_steps = ceil(0.6 * width / pixels)
            re_offset = origin.x % pixels
            for i in range(-re_steps, re_steps):
                # Store the tick x coordinate in screen space and global space.
                screen_tick = re_offset + i * pixels
                global_tick = (screen_tick - origin.x) / zoom
                if abs(global_tick) < 10**-10:  # Floats aren't perfect.
                    continue
                self.addItem(FlippedText(
                    "{:n}".format(global_tick),
                    width / 2 + screen_tick,
                    height / 2 + cling_y))
                self.addLine(
                    width / 2 + screen_tick,
                    height / 2 + cling_y + TICK_SIZE,
                    width / 2 + screen_tick,
                    height / 2 + cling_y - TICK_SIZE)

            im_steps = ceil(0.6 * height / pixels)
            im_offset = origin.y % pixels
            for i in range(-im_steps, im_steps):
                screen_tick = im_offset + i * pixels
                global_tick = (screen_tick - origin.y) / zoom
                if abs(global_tick) < 10**-10:
                    continue
                self.addItem(FlippedText(
                    "{:n}".format(global_tick),
                    width / 2 + cling_x,
                    height / 2 + screen_tick))
                self.addLine(
                    width / 2 + cling_x + TICK_SIZE,
                    height / 2 + screen_tick,
                    width / 2 + cling_x - TICK_SIZE,
                    height / 2 + screen_tick)

            # Only label origin if it is actually in viewport (not clinging).
            if cling_x - origin.x == 0 and cling_y - origin.y == 0:
                self.addItem(FlippedText(
                    "0",
                    width / 2 + cling_x,
                    height / 2 + cling_y
                ))

    def draw_plots(self):
        width = self.sceneRect().width()
        height = self.sceneRect().height()
        center = Point(width / 2, height / 2)

        offset = self.program.diagram.translation
        zoom = self.program.diagram.zoom
        stroke = self.program.preferences.stroke

        for i in range(self.program.diagram.plots.rowCount()):
            plot = self.program.diagram.plots.item(i)
            type = plot.data(ROLE_TYPE)
            relation = plot.data(ROLE_RELATION)
            shape = plot.data(ROLE_SHAPE)
            fill_color = plot.data(ROLE_COLOR)
            stroke_color = QColor(fill_color)
            stroke_color.setAlpha(255)

            pen = QPen(stroke_color)
            pen.setWidth(stroke)
            if relation in [REL_LESS, REL_MORE]:
                pen.setStyle(Qt.DashLine)

            brush = QBrush(fill_color)
            
            if isinstance(shape, Point) and type == TYPE_POINT:
                p = project(shape, offset, zoom) - Point(1, 1)
                self.addEllipse(
                    center.x + p.x, center.y + p.y,
                    2, 2, pen, QBrush(stroke_color))

            if isinstance(shape, Circle):
                if type == TYPE_CIRCLE:
                    self.addEllipse(
                        center.x + (shape.origin().x - offset.x) * zoom,
                        center.y + (shape.origin().y - offset.y) * zoom,
                        shape.diameter() * zoom, shape.diameter() * zoom, pen)

                if type == TYPE_DISK:
                    self.addEllipse(
                        center.x + (shape.origin().x - offset.x) * zoom,
                        center.y + (shape.origin().y - offset.y) * zoom,
                        shape.diameter() * zoom, shape.diameter() * zoom,
                        pen, brush)

                if type == TYPE_NEGATIVE_DISK:
                    pass

            if isinstance(shape, Line):
                if abs(shape.gradient) <= 1:
                    left = Line(float("inf"), -center.x / zoom + offset.x)
                    right = Line(float("inf"), center.x / zoom + offset.x)
                    p0 = shape.intersect(left)
                    p1 = shape.intersect(right)
                else:
                    bottom = Line(0, -center.y / zoom + offset.y)
                    top = Line(0, center.y / zoom + offset.y)
                    p0 = shape.intersect(bottom)
                    p1 = shape.intersect(top)
                q0 = project(p0, offset, zoom)
                q1 = project(p1, offset, zoom)

                if type == TYPE_LINE:
                    self.addLine(
                        center.x + q0.x, center.y + q0.y,
                        center.x + q1.x, center.y + q1.y)

                if type == TYPE_HALF_PLANE:
                    # Construct a polygon.
                    polygon = QPolygonF()
                    polygon.append(QPointF(center.x + q0.x, center.y + q0.y))
                    polygon.append(QPointF(center.x + q1.x, center.y + q1.y))
                    above = bool(shape.side & ABOVE) * 2 - 1
                    right = bool(shape.side & RIGHT) * 2 - 1
                    if abs(shape.gradient) <= 1:
                        polygon.append(QPointF(
                            center.x + q1.x,
                            center.y + (height/2 + 1) * above))
                        polygon.append(QPointF(
                            center.x + q0.x,
                            center.y + (height/2 + 1) * above))
                    else:
                        polygon.append(QPointF(
                            center.x + (width/2 + 1) * right,
                            center.y + q1.y))
                        polygon.append(QPointF(
                            center.x + (width/2 + 1) * right,
                            center.y + q0.y))

                    self.addPolygon(polygon, pen, brush)


            if isinstance(shape, Ray) or isinstance(shape, DualRay):            
                def find_intersections(ray, near, far):
                    """Try to intersect a ray with edges of the screen. If the
                       endpoint is on-screen, return it as an intersection.
                    """
                    p0 = ray.intersect(near)
                    p1 = ray.intersect(far)
                    if not p0 or not p1:
                        if not p0:
                            p0 = ray.endpoint
                        elif not p1:
                            p1 = ray.endpoint
                        else:
                            return None
                    return (p0, p1)

                def draw_ray(ray):
                    left = Line(float("inf"), -center.x / zoom + offset.x)
                    right = Line(float("inf"), center.x / zoom + offset.x)
                    bottom = Line(0, -center.y / zoom + offset.y)
                    top = Line(0, center.y / zoom + offset.y)
                    if pi / 4 <= ray.angle % pi < 3 * pi / 4:
                        points = find_intersections(ray, bottom, top)
                    else:
                        points = find_intersections(ray, left, right)
                    if not points[0] or not points[1]:
                        return
                    self.addLine(
                        center.x + (points[0].x - offset.x) * zoom,
                        center.y + (points[0].y - offset.y) * zoom,
                        center.x + (points[1].x - offset.x) * zoom,
                        center.y + (points[1].y - offset.y) * zoom, pen)

                if type == TYPE_RAY:
                    draw_ray(shape)

                if type == TYPE_DUAL_RAY:
                    for ray in shape.rays:
                        draw_ray(ray)

                if type == TYPE_SECTOR:
                    pass

    def set_viewport(self, viewport):
        """Called when the size of the parent widget changes."""
        self.setSceneRect(QRectF(viewport.geometry()))
