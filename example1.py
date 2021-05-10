import pygame
from pygame.locals import *

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

root = mymap.build_map([edge3, edge1, edge2, edge4])

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	