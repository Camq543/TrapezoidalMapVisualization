from TrapMap import *
from Edge import Edge
from Point import Point

mymap = TrapMap()

edge1 = Edge(Point(1,1), Point(3,1))
edge2 = Edge(Point(2,4), Point(4,2))
edge3 = Edge(Point(7,7), Point(10,10))
edge4 = Edge(Point(1.5,6), Point(8,6))

root = mymap.build_map([edge1, edge3, edge2, edge4])

print(len(mymap.trapezoid_list))
print(mymap.trapezoid_list)