import random
import time

import pygame

from Bounds import Bounds
from Trapezoid import Trapezoid
from Node import Node
from xNode import xNode
from yNode import yNode
from Leaf import Leaf
from Point import Point
from Edge import Edge

class TrapMap:
    def __init__(self, screen):
        self.trapezoid_list = []
        self.segment_list = []
        self.screen = screen
        self.bbox = Bounds(Point(0,0), Point(0,0), True, .1)
        self.width, self.height = pygame.display.get_window_size()
        self.margin = 10
        self.root = None
        self.pygame_config = {
            'screen' : screen,
            'width' : self.width,
            'height' : self.height
        }

    def build_map(self, segments):
        for segment in segments:
            pygame.display.flip()
            self.bbox.add_point(segment.left)
            self.bbox.add_point(segment.right)

        if self.bbox.is_empty():
            self.bbox.add_point(point(0,0))
            self.bbox.add_point(point(1,1))
        else:
            self.bbox.pad_bounds()

        random.shuffle(segments)

        root = Leaf(self.bbox.to_trapezoid())
        self.trapezoid_list.append(root.trapezoid)
        self.draw_trapezoid(self.bbox.to_trapezoid(), 'black')
        for segment in segments:
            root = self.add_edge(segment, root)
            self.segment_list.append(segment)

        for trapezoid in self.trapezoid_list:
            self.draw_trapezoid(trapezoid, 'black')
        for segment2 in self.segment_list:
            self.draw_edge(segment2, 'blue', 4)
        pygame.display.flip()

        self.root = root

    def build_box(self, segments):
        for segment in segments:
            pygame.display.flip()
            self.bbox.add_point(segment.left)
            self.bbox.add_point(segment.right)

        if self.bbox.is_empty():
            self.bbox.add_point(point(0,0))
            self.bbox.add_point(point(1,1))
        else:
            self.bbox.pad_bounds()

        root = Leaf(self.bbox.to_trapezoid())
        self.trapezoid_list.append(root.trapezoid)

        self.root = root

    def incremental_build(self, segment):
        self.root = self.add_edge(segment, self.root)
        self.segment_list.append(segment)


    def add_edge(self, edge, root):
        trapezoids = self.find_intersections(root, edge)

        # Need to hang on to the trapezoids that we just changed and/or created
        last_old = None
        last_below = None
        last_above = None

        for i in range(len(trapezoids)):
            old = trapezoids[i]

            is_first = i == 0
            is_last = i == len(trapezoids) - 1

            # Check for degenerate endpoints
            has_left = is_first and edge.left != old.left
            has_right = is_last and edge.right != old.right

            # First we update the trapezoids 
            if is_first and is_last:
                # Segment is completely enclosed by one trapezoid
                # We split the current trapezoid into four new ones:
                # left, right, above, and below segment
                # except in the degenerate case where trapezoids share a left or right
                if has_left:
                    left = Trapezoid(old.left, edge.left, old.top, old.bottom)
                above = Trapezoid(edge.left, edge.right, old.top, edge)
                below = Trapezoid(edge.left, edge.right, edge, old.bottom)
                if has_right:
                    right = Trapezoid(edge.right, old.right, old.top, old.bottom)

                # Now we update trapezoids with their new neighbors
                # Setting the neighbor of a trapezoid also updates its new neighbor
                if has_left:
                    left.set_upper_left(old.upper_left)
                    left.set_lower_left(old.lower_left)
                    left.set_upper_right(above)
                    left.set_lower_right(below)

                else:
                    above.set_upper_left(old.upper_left)
                    below.set_lower_left(old.lower_left)

                if has_right:
                    right.set_upper_left(above)
                    right.set_lower_left(below)
                    right.set_upper_right(old.upper_right)
                    right.set_lower_right(old.lower_right)

                else:
                    above.set_upper_right(old.upper_right)
                    below.set_lower_right(old.lower_right)

            elif is_first:
                # We are in the first trapezoid intersected
                # And the segment intersects more trapezoids
                # We make three new trapezoids: left, above, and below (barring left point degeneracy)
                # Ignore everything to the right of this trapezoid
                if has_left:
                    left = Trapezoid(old.left, edge.left, old.top, old.bottom)
                above = Trapezoid(edge.left, old.right, old.top, edge)
                below = Trapezoid(edge.left, old.right, edge, old.bottom)

                # Update neighbors
                if has_left:
                    left.set_upper_left(old.upper_left)
                    left.set_lower_left(old.lower_left)
                    left.set_upper_right(above)
                    left.set_lower_right(below)

                else:
                    above.set_upper_left(old.upper_left)
                    below.set_lower_left(old.lower_left)
                
                above.set_upper_right(old.upper_right)
                below.set_lower_right(old.lower_right)

            elif (not is_last) and not (is_first):
                # We are in a middle trapezoid being intersected
                # Need to merge this trapezoid into newly created left trapezoids
                # Or create new trapezoids, depending on current map
                if last_above.top == old.top:
                    # If the top trapezoid we just created shares a top edge with the current intersected trapezoid
                    # We need to merge the last created trapezoid with the current one
                    last_above.right = old.right
                    above = last_above
                else:
                    # Otherwise, we make a new trapezoid
                    above = Trapezoid(old.left, old.right, old.top, edge)

                if last_below.bottom == old.bottom:
                    # Same logic as the above trapezoid, but flipped vertically
                    last_below.right = old.right
                    below = last_below
                else:
                    below = Trapezoid(old.left, old.right, edge, old.bottom)

                # Update neighbors
                if above != last_above:
                    # If we made a new top trapezoid
                    above.set_lower_left(last_above)

                    if old.upper_left is last_old:
                        # If this intersected trapezoid shared an upper edge with the previous intersected trapezoid
                        above.set_upper_left(last_above)
                    else:
                        above.set_upper_left(old.upper_left)

                if below != last_below:
                    # If we made a new bottom trapezoid
                    below.set_upper_left(last_below)

                    if old.lower_left is last_old:
                        # If this intersected trapezoid shared a lower edge with the previous intersected trapezoid
                        below.set_lower_left(last_below)
                    else:
                        below.set_lower_left(old.lower_left)

                below.set_lower_right(old.lower_right)
                above.set_upper_right(old.upper_right)

            else:
                # We are in the last trapezoid being intersected 
                # And the segment intersected other trapezoids
                # Merge or create new trapezoids by same logic as middle
                if last_above.top == old.top:
                    last_above.right = edge.right
                    above = last_above
                else:
                    above = Trapezoid(old.left, edge.right, old.top, edge)

                if last_below.bottom == old.bottom:
                    last_below.right = edge.right
                    below = last_below
                else:
                    below = Trapezoid(old.left, edge.right, edge, old.bottom)

                if has_right:
                    right = Trapezoid(edge.right, old.right, old.top, old.bottom)

                # Update Neighbors
                if has_right:
                    right.set_upper_right(old.upper_right)
                    right.set_lower_right(old.lower_right)
                    right.set_upper_left(above)
                    right.set_lower_left(below)
                else:
                    above.set_upper_right(old.upper_right)
                    below.set_lower_right(old.lower_right)

                if above != last_above:
                    # If we made a new top trapezoid
                    above.set_lower_left(last_above)

                    if old.upper_left is last_old:
                        # If this intersected trapezoid shared an upper edge with the previous intersected trapezoid
                        above.set_upper_left(last_above)
                    else:
                        above.set_upper_left(old.upper_left)

                if below != last_below:
                    # If we made a new bottom trapezoid
                    below.set_upper_left(last_below)

                    if old.lower_left is last_old:
                        # If this intersected trapezoid shared a lower edge with the previous intersected trapezoid
                        below.set_lower_left(last_below)
                    else:
                        below.set_lower_left(old.lower_left)

            # Now we need to update the search structure
            # First create a y node pointing to above and below trapezoid
            if above == last_above:
                # If we didn't make a new top trapezoid
                # We need to reference the node associated with the last top trapezoid
                above_node = above.node
            else:
                # Otherwise we make a new leaf
                above_node = Leaf(above)

            # Do the same below
            if below == last_below:
                below_node = below.node
            else:
                below_node = Leaf(below)

            subtree_root = yNode(above_node, below_node, edge)
            if above not in self.trapezoid_list:
                self.trapezoid_list.append(above)

            if below not in self.trapezoid_list:
                self.trapezoid_list.append(below)

            if has_right:
                # If we're updating the last intersected trapezoid and made a new right trapezoid
                # We make a right xNode pointing to the new yNode
                subtree_root = xNode(subtree_root, Leaf(right), edge.right)
                if right not in self.trapezoid_list:
                    self.trapezoid_list.append(right)

            if has_left:
                # If we're updating the first intersected trapezoid and made a new left trapezoid
                # We make a left xNode pointing to the right xNode or new yNode
                subtree_root = xNode(Leaf(left), subtree_root, edge.left)
                if left not in self.trapezoid_list:
                    self.trapezoid_list.append(left)

            if old in self.trapezoid_list:
                self.trapezoid_list.remove(old)
            old_node = old.node
            if old_node is root:
                # If we just modified the root trapezoid 
                root = subtree_root
            else:
                # Swap old node for new one
                old_node.replace_self(subtree_root)

            if not is_last:
                last_old = old
                last_above = above
                last_below = below



        return root

    def find_intersections(self, rootNode, inEdge):
        toReturn = []
        trapezoid = rootNode.edge_search(inEdge)
        toReturn.append(trapezoid)

        while not inEdge.right.left_of(trapezoid.right):
            rel_pos = inEdge.above_or_below(trapezoid.right)
            if rel_pos < 0:
                # Edge is below trapezoid's right point
                trapezoid = trapezoid.lower_right
            elif rel_pos > 0:
                # Edge is above trapezoid's right point
                trapezoid = trapezoid.upper_right
            else:
                raise ValueError("Edges cannot intersect")

            if trapezoid is None:
                raise ValueError("No trapezoid to the right, uh oh")

            toReturn.append(trapezoid)

        return toReturn

    def pygame_coords(self, point):
        x_norm = (point.x - self.bbox.lowerLeft.x) / (self.bbox.upperRight.x - self.bbox.lowerLeft.x)
        x = self.margin + x_norm * (self.width - 2 * self.margin)

        y_norm = (point.y - self.bbox.lowerLeft.y) /(self.bbox.upperRight.y - self.bbox.lowerLeft.y)
        y = self.height - self.margin - y_norm * (self.height - 2 * self.margin)

        return (x, y)


    def draw_edge(self, edge, color = 'black', width = 1):
        pygame.draw.line(self.screen, color, self.pygame_coords(edge.left), self.pygame_coords(edge.right), width)
        

    def draw_trapezoid(self, trapezoid, color = 'black', width = 1):
        left_edge = Edge(Point(trapezoid.left.x, self.bbox.lowerLeft.y), Point(trapezoid.left.x, self.bbox.upperRight.y))
        right_edge = Edge(Point(trapezoid.right.x, self.bbox.lowerLeft.y), Point(trapezoid.right.x, self.bbox.upperRight.y))

        topLeft = self.pygame_coords(self.intersection_point(left_edge, trapezoid.top))
        bottomLeft = self.pygame_coords(self.intersection_point(left_edge, trapezoid.bottom))
        topRight = self.pygame_coords(self.intersection_point(right_edge, trapezoid.top))
        bottomRight = self.pygame_coords(self.intersection_point(right_edge, trapezoid.bottom))

        pygame.draw.line(self.screen, color, topLeft, topRight, width)
        pygame.draw.line(self.screen, color, topLeft, bottomLeft, width)
        pygame.draw.line(self.screen, color, topRight, bottomRight, width)
        pygame.draw.line(self.screen, color, bottomLeft, bottomRight, width)

    def draw_point(self, point, color = 'green', radius = 4, width = 0):
        pygame.draw.circle(self.screen, color, self.pygame_coords(point), radius, width)




    def intersection_point(self, edge1, edge2):
        line1 = tuple(edge1)
        line2 = tuple(edge2)

        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Point(x, y)

    def draw_trapezoids(self):
        for trapezoid in self.trapezoid_list:
            self.draw_trapezoid(trapezoid, 'black')

    def draw_segments(self):
        for segment in self.segment_list:
            self.draw_edge(segment, 'blue', 4)

