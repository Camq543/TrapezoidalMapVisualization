from Node import Node
from Trapezoid import Trapezoid
from Edge import Edge
from Point import Point


class Leaf(Node):

    def __init__(self, trapezoid):
        super().__init__()
        self.trapezoid = trapezoid
        trapezoid.node = self

    def __eq__(self, other):
        return self.trapezoid == other.trapezoid

    def edge_search(self, inEdge):
        return self.trapezoid

    def point_search(self, inPoint):
        return self.trapezoid

    def provenance_search(self, inPoint, path):
        path.append(self.trapezoid)
        return self.trapezoid

