from Node import Node
from Trapezoid import Trapezoid
from Edge import Edge
from Point import Point


class xNode(Node):

    def __init__(self, left, right, point):
        super().__init__()
        self.left = left
        self.right = right
        self.point = point
        self.left.add_parent(self)
        self.right.add_parent(self)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.point == other.point

    def point_search(self, inPoint):
        if self.point == inPoint:
            return self.point
        elif self.point.left_of(inPoint):
            return self.right.point_search(inPoint)
        else:
            return self.left.point_search(inPoint)

    def provenance_search(self, inPoint, path):
        path.append(self.point)
        if self.point == inPoint:
            return self.point
        elif self.point.left_of(inPoint):
            return self.right.provenance_search(inPoint, path)
        else:
            return self.left.provenance_search(inPoint, path)

    def edge_search(self, inEdge):
        if self.point == inEdge.left:
            return self.right.edge_search(inEdge)
        elif self.point.left_of(inEdge.left):
            return self.right.edge_search(inEdge)
        else:
            return self.left.edge_search(inEdge)


    def swap_child(self, oldNode, newNode):
        if newNode is None:
            raise ValueError("New node is Null")
        if self.right is oldNode:
            self.right = newNode
        elif self.left is oldNode:
            self.left = newNode
        else:
            raise ValueError("Node to replace is not a child")

        oldNode.remove_parent(self)
        newNode.add_parent(self)


