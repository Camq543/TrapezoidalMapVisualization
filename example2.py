import pygame
from pygame.locals import *

import time

from TrapMap import *
from Edge import Edge
from Point import Point

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
					# time.sleep(1)
				elif edge_drawn:
					mymap.incremental_build(edge)
					screen.fill('white')
					mymap.draw_trapezoids()
					mymap.draw_segments()
					pygame.display.flip()
					edge_drawn = False
					edge_index += 1
					# time.sleep(1)






	