class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return(self.x == other.x and self.y == other.y)

    def __str__(self):
        return "(" + '{:.2f}'.format(self.x) + "," + '{:.2f}'.format(self.y) + ")"

    def __iter__(self):
        yield self.x
        yield self.y


    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def left_of(self, other):
        return ((self.x, self.y) < (other.x, other.y))    


