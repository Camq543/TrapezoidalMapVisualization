from Node import Node
from Trapezoid import Trapezoid
from Edge import Edge
from Point import Point


class yNode(Node):

    def __init__(self, above, below, edge):
        super().__init__()
        self.above = above
        self.below = below
        self.edge = edge
        self.above.add_parent(self)
        self.below.add_parent(self)

    def __eq__(self, other):
        return self.above == other.above and self.below == other.below and self.edge == other.edge

    def point_search(self, inPoint):
        rel_position = self.edge.above_or_below(inPoint)
        if rel_position < 0:
            return self.above.point_search(inPoint)
        elif rel_position > 0:
            return self.below.point_search(inPoint)
        else:
            return self.edge

    def provenance_search(self, inPoint, path):
        path.append(self.edge)
        rel_position = self.edge.above_or_below(inPoint)
        if rel_position < 0:
            return self.above.provenance_search(inPoint, path)
        elif rel_position > 0:
            return self.below.provenance_search(inPoint, path)
        else:
            return self.edge

    def edge_search(self, inEdge):

        if self.edge.left == inEdge.left:
            # We share a left point with the input edge
            if self.edge.get_slope() == inEdge.get_slope():
                return None
            if self.edge.get_slope() > inEdge.get_slope():
                return self.below.edge_search(inEdge)
            else:
                return self.above.edge_search(inEdge)

        elif self.edge.right == inEdge.right:
            # We share a right point with the input edge
            if self.edge.get_slope() == inEdge.get_slope():
                return None
            if self.edge.get_slope() < inEdge.get_slope():
                return self.below.edge_search(inEdge)
            else:
                return self.above.edge_search(inEdge)

        else:
            relative_position = self.edge.above_or_below(inEdge.left)
            if relative_position < 0:
                return self.above.edge_search(inEdge)
            elif relative_position > 0:
                return self.below.edge_search(inEdge)
            else:
                raise ValueError("Edges cannot intersect")


    def swap_child(self, oldNode, newNode):
        if newNode is None:
            raise ValueError("New node is Null")
        if self.above is oldNode:
            self.above = newNode
        elif self.below is oldNode:
            self.below = newNode
        else:
            raise ValueError("Node to replace is not a child")

        oldNode.remove_parent(self)
        newNode.add_parent(self)

