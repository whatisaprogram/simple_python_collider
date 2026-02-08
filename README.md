SIMPLE PYTHON COLLIDER

This module allows you to define four kinds of "shapes" as they exist on some coordinate plane: Points, Circles, Squares, and Othergons. 
You may then call Shape1.collide(Shape2), and the returned result will be a boolean representing whether or not a collision is
happening between these two shapes.

Point Objects:
Point objects accept one positional arguments to instantiate: "location." This represents the location of a point in an arbitrary 
2D space. Since this is Python, there is no requirement for the point to be a specific data structure, only that it is indexable and
that the x coordinate is in index 0, and that the y coordinate is in index 1.

Circle Objects:
Circle objects accept two positional arguments to instantiate: "center" and "radius." This represents the location of the center of a
circle (again, in format (x,y)--any indexable format is OK) and the length of its radius.

Square Objects:
Square objects represent axis-aligned rectangles (though they are called squares.) It really does have to be the case that the
rectangle as to be "straight"--if the rectangle is rotated in any way, Othergons should be used. Square objects accept one positional
argument: a list of vertices in format (x,y) ordered by their connections to each other. It does not matter which vertex is "first,"
only that they are ordered correctly.

Othergon Objects:
Othergon Objects represent all convex polygons (including Square objects but excluding points; the code will run erroneously if you attempt
to give it a 1-vertex polygon; please use the Point class instead.) Like Square objects, they accept one positional argument: a list of
(x,y) coordinates representing the vertices in order of their connections. If the vertices are unordered, the file will not work.

On Concave Polygons:
All concave polygons can be deconstructed into many convex ones; they must be represented with multiple Othergon objects.
