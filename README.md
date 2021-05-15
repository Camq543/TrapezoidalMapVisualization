# TrapezoidalMapVisualization
A visualization of a randomized incremental trapezoidal map decomposition

##Description
This project is an implementation of the trapezoidal map decomposition algorithm described in the **Computational Geometry, Algorithms and Applications 3rd Edition textbook.** Given a set of non-vertical, non-intersecting segments, the algorithm constructs a decomposition to quickly find the area containing a given point. No two endpoints of segments can share an x coordinate. The algorithm consists of two parts, a data structure storing a trapezoidal decomposition of the space, and a data structure for searching the map. For a more detailed description of the algorithm’s process, see it’s description in **Computational Geometry, Algorithms and Applications 3rd Edition** starting on page 122. 
The segments are visualized in blue, while the added decomposition is drawn in black. 

##Running the Program
To run the program, you need python 3 installed with the pygame package. After initializing a pygame screen, you initialize the TrapMap class by passing it the pygame screen. Next, the map is constructed by giving it a set of non-intersecting, non-vertical edges (made of the edge class). This can be done all at once by calling the build_map method, or incrementally, by first calling the build_box method, and then the incremental_build method for each segment. An example of the full build can be found in example1.py, and the incremental build in example 2 and 3. Example 4 and 5 both demonstrate the point location process. The point being searched for is in green, and the process of finding that point in red. Example 6 shows a construction and point search for a much larger number (set at 30) of randomly generated segments. Note that segment generation is done inefficiently, and may take a long time for an arbitrarily large number of segments. 

##Construction
The decomposition is constructed by incrementally adding individual segments in a random order. As each segment is added, the algorithm searches through the search structure to find all trapezoids intersected by the segment being added. After finding a list of trapezoids that need to be added, the algorithm proceeds from left to right along this list, creating, merging, and deleting existing trapezoids as necessary. At each step, the search structure is updated accordingly when a trapezoid is added or changed. 

For easy visualization purposes, the algorithm maintains a list of all the segments and trapezoids. This will affect construction time complexity, so the algorithm may not perform as expected. 


##Complexity
Without a randomized segment order, construction can take a very long time, with *n* segments being added and each segment taking a linear amount of time to update the structures, leading to O(*n*<sup>2</sup>) time complexity. However, with randomized segment order the expected construction time for the decomposition and search structure is O(*n* log *n*). 
Space complexity for the map is limited to a maximum of 6n + 4 vertices, and 3n + 4 trapezoids, giving a worst-case space complexity of O(*n*). For the search structure, unlucky construction order could give O(*n*<sup>2</sup>) space, but on average a constant amount of nodes will be added for each segment, leading to an expected space complexity of O(*n*). 
Query time for the search structure is O(*n* log *n*).

##My Implementation 
The algorithm is implemented in Python, using the Pygame library for visualization. It consists of 8 different classes (and one abstract node class), namely a class for each of: point, edge, bounding box, trapezoid, x node, y node, leaf node, and the map itself. All of the construction algorithm can be found in the TrapMap class. 
