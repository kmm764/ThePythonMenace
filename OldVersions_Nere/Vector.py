import math


class Vector:

    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        """
        This method modifies the addition predefined method
        """
        return Vector(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        """
         This method modifies the subtraction predefined method
        """
        return Vector(self[0] - other[0], self[1] - other[1])

    def __iadd__(self, other):
        """
            This method modifies the addition with assignment predefined method
        """
        self.x = other[0] + self.x
        self.y = other[1] + self.y
        return self

    def __isub__(self, other):
        """
            This method modifies the subtraction with assignment predefined method
        """
        self.x = other[0] + self.x
        self.y = other[1] + self.y
        return self

    def div_cte(self, const):
        return Vector(self[0] / const, self[1] / const)

    def times(self, const):
        return Vector(self[0] * const, self[1] * const)

    def module(self):
        """
            This method returns the module of the vector
        """
        return math.sqrt(self.x*self.x + self.y*self.y)

    def arg(self):
        """
            This method returns the argument of the vector
        """
        return math.atan2(self.x, self.y)

    def unit(self):
        """
            This method returns a unit vector with the same direction of the vector that calls the method
        """
        if self.module()!= 0:
            return Vector(self.x/self.module(),self.y/self.module())
        else:
            return Vector(0, 0)

    def __idiv__(self, other):
        self[0] = self[0] / other
        self[1] = self[1] / other
        return self

    def __imul__(self, other):
        self[0] = self[0] * other
        self[1] = self[1] * other
        return self

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise Exception("Invalid index")

    def __str__(self):
        return "({},{})".format(self.x, self.y)
"""
    def __setitem__(self, key, value):
        if (key == 0):
            self.x = value
        elif (key == 1):
            self.y = value
        else:
            raise Exception("Invalid index")
"""


