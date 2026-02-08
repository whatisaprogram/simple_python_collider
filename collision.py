# collision.py
import math
import numpy

'''
usage:
depending on the type of shape, you can instantiate Point objects, axis-aligned Square (really, rectangle) objects, Circle objects, and 
"Othergon" (convex polygon) Objects.
then you can test if they collide with object1.collides(object2) as long as object1 and object2 are in [Square, Point, Circle, Othergon]

for example:
circle1 = Circle([0,0], 3) #Circle(center, radius)
square1 = Square([[1, 1], [4,4], [1, 4], [4,1]]) #Square(list of 2D corners)
booleany = circle1.collide(square1)
booleany in this case will return true

this file only tells you if two objects you create with it collide. create other classes to track their speed, behavior during collision,
etc. 
'''
class Collidable:

    def collide(self, other):
        if isinstance(other, Point):
            return self.with_point(other)
        elif isinstance(other, Circle):
            return self.with_circle(other)
        elif isinstance(other, Square):
            return self.with_square(other)
        else:
            return self.with_othergon(other)


    def with_point(self, other):
        pass

    def with_circle(self, other):
        pass
    
    def with_square(self, other):
        pass

    def with_othergon(self, other):
        pass
    
    
class Point(Collidable):
    def __init__(self, location):
        super().__init__()
        self.location = location

    def with_point(self, other):
        #simply check if the other has the same location
        return True if self.location == other.location else False

    def with_circle(self, other):
        return True if math.hypot(self.location[0] - other.center[0], self.location[1] - other.center[1]) < other.radius else False
    
    def with_square(self, other):
        return True if other.horizontal_span[0] <= self.location[0] <= other.horizontal_span[1] and other.vertical_span[0] <= self.location[1] <= other.vertical_span[1] else False
    
    def with_othergon(self, other):
        return other.with_point(self)
        

class Circle(Collidable):
    def __init__(self, center, radius):
        super().__init__()
        self.center = center
        self.radius = radius

    def with_point(self, other):
        return other.with_circle(self)

    def with_circle(self, other):
        return True if math.hypot(self.center[0] - other.center[0], self.center[1] - other.center[1]) <= self.radius + other.radius else False
    
    def with_square(self, other):
        return other.with_circle(self)
    
    def with_othergon(self, other):
        return other.with_circle(self)
    
class Square(Collidable):
    def __init__(self, corners):
        super().__init__()
        xs = [x[0] for x in corners]
        ys = [y[1] for y in corners]
        self.corners = corners
        self.horizontal_span = (min(xs), max(xs))
        self.vertical_span = (min(ys), max(ys))
 
    def with_point(self, other):
        return other.with_square(self)

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
    
    def with_othergon(self, other):
        return other.with_square(self)

class Othergon(Collidable):
    def __init__(self, vertices):
        super().__init__()
        self.vertices = vertices
        #assume they are in order (must be convex but doesn't have to be a regular polygon)
        self.normals = []
        for i in range(len(self.vertices) - 1):
            self.normals.append([self.vertices[i][0]-self.vertices[i+1][0], self.vertices[i][1]-self.vertices[i+1][1]])
        self.normals.append([self.vertices[0][0]-self.vertices[-1][0], self.vertices[0][1]-self.vertices[-1][1]])
        for vector in self.normals:
            temp = vector[1]
            vector[1] = -vector[0]
            vector[0] = temp
        removals = []
        for vector in self.normals:
            distance = math.hypot(vector[0], vector[1])
            if distance == 0:
                removals.append([vector[0], vector[1]])
                #should be an error message here since this would be a user error.
                continue
            vector[1] = vector[1]/distance
            vector[0] = vector[0]/distance
        for a_removal in removals:
            self.normals.remove(a_removal)
    
        self.vertices = numpy.array(self.vertices)
        self.normals = numpy.array(self.normals)

    def with_othergon(self, other):
        normals = numpy.concatenate([self.normals, other.normals], axis=0)
        shadows_self = self.vertices @ normals.transpose()
        shadows_other = other.vertices @ normals.transpose()

        min_self = shadows_self.min(axis=0)
        max_self = shadows_self.max(axis=0)
        min_other = shadows_other.min(axis=0)
        max_other = shadows_other.max(axis=0)

        for j in range(len(max_other)):
            if max_self[j] < min_other[j] or min_self[j] > max_other[j]:
                return False
        return True

    def with_point(self, other):
        normals = self.normals
        shadows_self = self.vertices @ normals.transpose()
        shadows_other = numpy.array(other.location).reshape(1, 2) @ normals.transpose()

        min_self = shadows_self.min(axis=0)
        max_self = shadows_self.max(axis=0)
        min_other = shadows_other.min(axis=0)
        max_other = shadows_other.max(axis=0)

        for j in range(len(max_other)):
            if max_self[j] < min_other[j] or min_self[j] > max_other[j]:
                return False
        return True

    def with_circle(self, other):
        C = numpy.array(other.center)
        closest_points_on_edge = []
        for i in range(len(self.vertices)):
            A = self.vertices[i]
            B = self.vertices[(i+1) % len(self.vertices)]
            AB = B - A
            AC = C - A
            t = numpy.clip((AC @ AB)/(AB @ AB), 0 , 1)
            closest_points_on_edge.append(A + t * (B-A))

        real_closest_point = [numpy.asarray([numpy.inf, numpy.inf]), numpy.inf]
        for closest_point in closest_points_on_edge:
            if numpy.linalg.norm(closest_point - C) < real_closest_point[1]:
                real_closest_point = [closest_point, numpy.linalg.norm(closest_point-C)]

        real_closest_point = real_closest_point[0]
        if numpy.linalg.norm(real_closest_point - C) == 0:
            return True
        axis = (real_closest_point - C) / numpy.linalg.norm(real_closest_point - C)



        normals = numpy.concatenate([self.normals, axis.reshape(1,2)], axis=0)

        shadows_self = self.vertices @ normals.transpose()
        shadows_other = C @ normals.transpose()

        min_self = shadows_self.min(axis=0)
        max_self = shadows_self.max(axis=0)
        min_other = shadows_other - other.radius
        max_other = shadows_other + other.radius

        for j in range(normals.shape[0]):
            if max_self[j] < min_other[j] or max_other[j] < min_self[j]:
                return False

        return True

    def with_square(self, other):
        square_othered = Othergon(other.corners)
        return self.with_othergon(square_othered)



