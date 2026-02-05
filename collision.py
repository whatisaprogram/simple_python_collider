# collision.py
import math
import numpy

'''
usage:
depending on the type of shape, you can instantiate Point objects, Square (really, rectangle) objects, and Circle objects
then you can test if they collide with object1.collides(object2) as long as object1 and object2 are in [Square, Point, Circle]

for example:
circle1 = Circle([0,0], 3, [0,0]) #Circle(center, radius, speed of object)
square1 = Square([[1, 1], [4,4], [1, 4], [4,1]]) #Square(list of 2D corners, speed omitted and assumed to be [0,0])
booleany = circle1.collide(square1)
booleany in this case will return true
'''
class Collidable:
    def __init__(self, speed=None):
        self.speed = speed or [0,0]


    def collide(self, other):
        if isinstance(other, Point):
            return self.with_point(other)
        elif isinstance(other, Circle):
            return self.with_circle(other)
        else:
            return self.with_square(other)


    def with_point(self, other):
        pass

    def with_circle(self, other):
        pass
    
    def with_square(self, other):
        pass
    
    
class Point(Collidable):
    def __init__(self, location, speed=None, position=None):
        super().__init__(speed or [0,0])
        self.location = location

    def with_point(self, other):
        #simply check if the other has the same location
        return True if self.location == other.location else False

    def with_circle(self, other):
        return True if math.hypot(self.location[0] - other.center[0], self.location[1] - other.center[1]) < other.radius else False
    
    def with_square(self, other):
        return True if other.horizontal_span[0] <= self.location[0] <= other.horizontal_span[1] and other.vertical_span[0] <= self.location[1] <= other.vertical_span[1] else False
        

class Circle(Collidable):
    def __init__(self, center, radius, speed=None):
        super().__init__(speed or [0,0])
        self.center = center
        self.radius = radius

    def with_point(self, other):
        return other.with_circle(self)

    def with_circle(self, other):
        return True if math.hypot(self.center[0] - other.center[0], self.center[1] - other.center[1]) <= self.radius + other.radius else False
    
    def with_square(self, other):
        return other.with_circle(self)
    
class Square(Collidable):
    def __init__(self, corners, speed=None):
        super().__init__(speed or [0,0])
        xs = [x[0] for x in corners]
        ys = [y[1] for y in corners]
        self.corners = corners
        self.horizontal_span = (min(xs), max(xs))
        self.vertical_span = (min(ys), max(ys))
 
    def with_point(self, other):
        return other.with_point(self)

    def with_circle(self, other):
        #first pick the closest point to the circle.
        closest_x = numpy.clip(other.center[0], self.horizontal_span[0], self.horizontal_span[1])
        closest_y = numpy.clip(other.center[1], self.vertical_span[0], self.vertical_span[1])

        #calculate the distance between the center and this point
        distance = math.hypot(closest_x - other.center[0], closest_y - other.center[1])

        if distance <= other.radius:
            return True
        else:
            return False
    
    def with_square(self, other):
        #horizontal and vertical spans overlap
        return self.horizontal_span[0] <= other.horizontal_span[1] and self.horizontal_span[1] >= other.horizontal_span[0] and self.vertical_span[0] <= other.vertical_span[1] and self.vertical_span[1] >= other.vertical_span[0]
    
