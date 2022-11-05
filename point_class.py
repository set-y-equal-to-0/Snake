from functools import reduce
import math as m

class V2:

    def __init__(self, x, y):

        self.v = (x, y)
        self.x = x
        self.y = y     

    def __add__(self, other):
        return V2(*(a + b for a, b in zip(self.v, other.v)))

    def __sub__(self, other):
        return V2(*(a - b for a, b in zip(self.v, other.v)))

    def __mul__(self, other):
        return reduce(lambda v0, v1: v0 + v1, (a * b for a, b in zip(self.v, other.v)))

    def __repr__(self):
        return f"{self.v}"

    def __eq__(self, other):
        return self.v == other.v

    def __abs__(self):
        return m.sqrt(self.x**2 + self.y**2)

    def __len__(self):
        return abs(self.x) + abs(self.y)

    def __hash__(self):
        return hash(self.v)




