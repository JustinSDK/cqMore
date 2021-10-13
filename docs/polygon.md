# `cqmore.polygon`

Provide functions for creating simple polygons.

## Functions

 Signature | Description
--|--
[`taiwan(h[,distance])`](polygon.md#taiwan) | Create a convex hull through the provided points. 
[`hull2D(points)`](polygon.md#hull2D) | Create a convex hull through the provided points. 

----

# `taiwan`

Create a Taiwan profile.

## Parameters

- `h` : The height of Taiwan.
- `distance = 0` : used for simplifying the shape. If the distance between a point and its previous points is not greater than distance, the point will be kept. 

## Examples 

    from cqmore import Workplane
    from cqmore.polygon import taiwan

    taiwan = (Workplane()
                .makePolygon(taiwan(20))
                .extrude(1)
            )

![taiwan](images/polygon_taiwan.JPG)

# `hull2D`

Create a convex hull through the provided points.

## Parameters

- `points`: the list of x, y points. 

## Examples     

    from random import random
    from cqmore import Workplane
    from cqmore.polygon import hull2D

    points = [(random(), random()) for i in range(20)]
    convex_hull = Workplane().makePolygon(hull2D(points)) 

![hull2D](images/polygon_hull2D.JPG)

