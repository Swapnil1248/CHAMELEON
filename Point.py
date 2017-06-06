import math
class Point:

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.isVisited = False

    def euclidean_distance(self, p):
        a = float(self.x) - p.x
        b = float(self.y) - p.y
        distance = math.sqrt(a*a + b*b)

        return distance

    def is_same(self, p):
        return self.x == p.x and self.y == p.y

    def __hash__(self):
        return hash(self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not(self == other)