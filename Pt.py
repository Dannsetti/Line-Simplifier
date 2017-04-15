import math

class Pt():
    def __init__(self,x,y):
          self._x = x
          self._y = y

    def getX(self):
         return self._x

    def getY(self):
         return self._y

    def EuclideanDistance(self,other):
        return math.sqrt ((self.getX() - other.getX())**2 + (self.getY() - other.getY())**2)

