import copy

from Trapezoid import Trapezoid
from Point import Point
from Edge import Edge

class Bounds:

    def __init__(self, upperRight, lowerLeft, isEmpty, padding):
        self.upperRight = upperRight
        self.lowerLeft = lowerLeft
        self.isEmpty = isEmpty
        self.padding = padding

    def __eq__(self, other):
        return self.lowerLeft == other.lowerLeft and self.upperRight == other.upperRight and self.empty == other.empty

    def __str__(self):
        return('Bounding Box with lower left corner at ' + str(self.lowerLeft) + ' and upper right at ' + str(self.upperRight))

    def is_empty(self):
        return self.isEmpty

    def pad_bounds(self):
        y_range = self.upperRight.y - self.lowerLeft.y
        x_range = self.upperRight.x - self.lowerLeft.y
        delta = Point(x_range * self.padding, y_range * self.padding)

        self.lowerLeft -= delta
        self.upperRight += delta

    def to_trapezoid(self):
        upperLeft = Point(self.lowerLeft.x, self.upperRight.y)
        lowerRight = Point(self.upperRight.x, self.lowerLeft.y)

        top = Edge(upperLeft, self.upperRight)
        bottom = Edge(self.lowerLeft, lowerRight)

        return Trapezoid(self.lowerLeft, self.upperRight, top, bottom)

    def add_point(self, inPoint):
        if self.is_empty():
            self.isEmpty = False
            self.lowerLeft = copy.copy(inPoint)
            self.upperRight = copy.copy(inPoint)

        else:
            if inPoint.x < self.lowerLeft.x:
                self.lowerLeft.x = inPoint.x
            elif inPoint.x > self.upperRight.x:
                self.upperRight.x = inPoint.x
            if inPoint.y < self.lowerLeft.y:
                self.lowerLeft.y = inPoint.y
            elif inPoint.y > self.upperRight.y:
                self.upperRight.y = inPoint.y



