import pygame
from pygame.locals import *

from TrapMap import *
from Edge import Edge
from Point import Point
from Trapezoid import Trapezoid

pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((960,960))

screen.fill('white')
pygame.display.flip()

running = True

mymap = TrapMap(screen)

edge1 = Edge(Point(1,1), Point(3,1))
edge2 = Edge(Point(2,4), Point(4,2))
edge3 = Edge(Point(7,7), Point(10,10))
edge4 = Edge(Point(1.5,6), Point(8,6))
edges = [edge1, edge2, edge3, edge4]
random.shuffle(edges)

mymap.build_box(edges)
mymap.draw_trapezoids()
pygame.display.flip()

search_point = Point(2.5, 2.5)
path_index = 0

edge_index = 0
edge_drawn = False

# result = mymap.root.point_search(search_point)
# print(result)

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
		
