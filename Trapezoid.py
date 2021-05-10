from Point import Point
from Edge import Edge

class Trapezoid:

    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.upper_left = None
        self.lower_left = None
        self.upper_right = None
        self.lower_right = None

        self.node = None

    def __eq__(self, other):
        if other is None:
            return NotImplemented
        return self.left == other.left and self.right == other.right and self.top == other.top and self.bottom == other.bottom

    def __str__(self):
        return "Top: " + str(self.top) + "\nBottom: " + str(self.bottom) + "\nLeft: " + str(self.left) + "\nRight" + str(self.right)

    def get_upper_left(self):
        return self.upper_left

    def set_upper_left(self, other):
        self.upper_left = other

        if other is not None:
            other.upper_right = self

    def get_upper_right(self):
        return self.upper_right

    def set_upper_right(self, other):
        self.upper_right = other

        if other is not None:
            other.upper_left = self

    def get_lower_left(self):
        return self.lower_left

    def set_lower_left(self, other):
        self.lower_left = other

        if other is not None:
            other.lower_right = self

    def get_lower_right(self):
        return self.lower_right

    def set_lower_right(self, other):
        self.lower_right = other

        if other is not None:
            other.lower_left = self



