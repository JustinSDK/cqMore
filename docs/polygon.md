# `cqmore.polygon`

Provide functions for creating simple polygons.

## Functions

 Signature | Description
--|--
[`hull2D(points)`](polygon.md#hull) | Create a convex hull through the provided points. 

----

# `hull2D`

Create a convex hull through the provided points.

## Parameters

- `points`: the list of x, y points. 

## Examples     

    from random import random
    from cqmore import Workplane
    from polygon import hull2D

    points = [(random(), random()) for i in range(20)]
    convex_hull = Workplane().makePolygon(*hull2D(points)) 

![hull2D](images/polygon_hull2D.JPG)

