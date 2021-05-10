from Point import Point

class Edge:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return "Edge from " + str(self.left) + " to " + str(self.right)

    def __iter__(self):
        yield(tuple(self.left))
        yield(tuple(self.right))

    def above_or_below(self, inPoint):
        v1 = (self.right.x - self.left.x, self.right.y - self.left.y)
        v2 = (self.right.x - inPoint.x, self.right.y - inPoint.y)

        cross = v1[0] * v2[1] - v1[1] * v2[0]

        if cross > 0:
            # edge is above point
            return 1

        elif cross < 0:
            # edge is below point
            return -1

        else:
            # point on line
            return 0

    def get_slope(self):
        if self.left.x == self.right.x:
            raise ValueError("No vertical segments allowed")
        diff = self.right - self.left
        return diff.y / diff.x
