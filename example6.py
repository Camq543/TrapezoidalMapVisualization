import pygame
from pygame.locals import *
import random

import time

from TrapMap import *
from Edge import Edge
from Point import Point

def check_intersection(edge1, edge2):
    line1 = tuple(edge1)
    line2 = tuple(edge2)

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return 0

    def on_segment(e1, p):
        p1 = e1.left
        p2 = e1.right
        return min(p1.x, p2.x) <= p.x <= max(p1.x, p2.x) and min(p1.y, p2.y) <= p.y <= max(p1.y, p2.y)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    intersect = Point(x,y)


    if (intersect == edge1.left or intersect == edge1.right) and (intersect == edge2.left or intersect == edge2.right):
        return 0

    elif on_segment(edge1, intersect) or on_segment(edge2, intersect):
        return 1

    else:
        return 0

    
def generate_segment(xlim, ylim, current_x):
    _random = random.Random(time.time())
    x1 = _random.randrange(0, xlim)
    while x1 in current_x:
        x1 = _random.randrange(0, xlim)
    # current_x[x1] = 1

    x2 = _random.randrange(0, xlim)
    while (x2 in current_x) or (x2 == x1):
        x2 = _random.randrange(0, xlim)
    # current_x[x2] = 1
    
    y1 = _random.randrange(0, ylim)
    y2 = _random.randrange(0,ylim)

    point1 = Point(x1, y1)
    point2 = Point(x2, y2)

    if point1.left_of(point2):
        return Edge(Point(x1, y1), Point(x2, y2))
    else:
        return Edge(Point(x2, y2), Point(x1, y1))

def generate_segments(num_segments, xlim, ylim):
    current_x = {}
    segments = []
    while len(segments) < num_segments:
        # print(len(segments))
        # print('generating')
        new_seg = generate_segment(xlim, ylim, current_x)
        # print(new_seg)
        intersection = False
        for segment in segments:
            # print(segment)
            intersection = check_intersection(segment, new_seg)
            # print(intersection)
            if intersection:
                break
        if intersection:
            continue
        else:
            segments.append(new_seg)
            current_x[new_seg.left.x] = 1
            current_x[new_seg.right.x] = 1

    return segments

print('generating segments')
edges = generate_segments(30, 100, 100)
print('segments generated, generating decomposition')
random.shuffle(edges)

pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((960,960))

screen.fill('white')
pygame.display.flip()

running = True

mymap = TrapMap(screen)

search_point = Point(25, 25)
path_index = 0

mymap.build_box(edges)
print(mymap.bbox)
mymap.draw_trapezoids()
pygame.display.flip()

edge_index = 0
edge_drawn = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if edge_index < len(edges):
                edge = edges[edge_index]
                if not edge_drawn:
                    screen.fill('white')
                    mymap.draw_trapezoids()
                    mymap.draw_segments()
                    mymap.draw_edge(edge, 'red', 4)
                    pygame.display.flip()
                    edge_drawn = True
                elif edge_drawn:
                    mymap.incremental_build(edge)
                    screen.fill('white')
                    mymap.draw_trapezoids()
                    mymap.draw_segments()
                    pygame.display.flip()
                    edge_drawn = False
                    edge_index += 1
                if edge_index == len(edges):
                    mymap.draw_point(search_point, 'green', 8)
                    pygame.display.flip()
                    path = []
                    result = mymap.root.provenance_search(search_point, path)
            elif path_index < len(path):
                toDraw = path[path_index]
                screen.fill('white')
                mymap.draw_trapezoids()
                mymap.draw_segments()
                mymap.draw_point(search_point, 'green', 8)
                if isinstance(toDraw, Point):
                    mymap.draw_point(toDraw, 'red', 8)
                elif isinstance(toDraw, Edge):
                    mymap.draw_edge(toDraw, 'red', 4)
                elif isinstance(toDraw, Trapezoid):
                    mymap.draw_trapezoid(toDraw, 'red', 4)
                pygame.display.flip()
                path_index += 1
