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

mymap.build_map([edge3, edge1, edge2, edge4])

point_drawn = False
point_index = 0
points = [Point(2.5,2.5), Point(5,5), Point(2,1), Point(8,6)]

# result = mymap.root.point_search(search_point)
# print(result)

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if point_index < len(points):
				point = points[point_index]
				if not point_drawn:
					screen.fill('white')
					mymap.draw_trapezoids()
					mymap.draw_segments()
					mymap.draw_point(point, 'green', 8)
					pygame.display.flip()
					point_drawn = True
					# time.sleep(1)
				elif point_drawn:
					screen.fill('white')
					mymap.draw_trapezoids()
					mymap.draw_segments()
					result = mymap.root.point_search(point)
					if isinstance(result, Point):
						mymap.draw_point(result, 'red', 8)
					elif isinstance(result, Edge):
						mymap.draw_edge(result, 'red', 4)
					elif isinstance(result, Trapezoid):
						mymap.draw_trapezoid(result, 'red', 4)
					pygame.display.flip()
					point_drawn = False
					point_index += 1
					# time.sleep(1)

