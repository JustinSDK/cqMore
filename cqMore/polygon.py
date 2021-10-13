"""
Provide functions for creating simple polygons.

"""

from typing import Iterable, cast

from .cq_typing import Point2D, VectorLike
from .util import toTuples


def hull2D(points: Iterable[VectorLike]) -> list[Point2D]:
    """
    Create a convex hull through the provided points.

    ## Parameters

    - `points`: the list of x, y points. 

    ## Examples 

        from random import random
        from cqmore import Workplane
        from polygon import hull2D

        points = [(random(), random()) for i in range(20)]
        convex_hull = Workplane().makePolygon(*hull2D(points))

    """

    def _cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # only need x, y 
    pts = [(p[0], p[1]) for p in sorted(toTuples(points))]
    leng = len(pts)
    convex_hull = [pts[0], pts[1]]

    # lower bound
    for i in range(2, leng):
        while len(convex_hull) >= 2 and _cross(convex_hull[-2], convex_hull[-1], pts[i]) <= 0:
            convex_hull.pop()
        convex_hull.append(pts[i])
    
    # upper bound
    upper_bound_start = len(convex_hull) + 1
    for i in range(leng - 2, -1, -1):
        while len(convex_hull) >= upper_bound_start and _cross(convex_hull[-2], convex_hull[-1], pts[i]) <= 0:
            convex_hull.pop()
        convex_hull.append(pts[i])
    convex_hull.pop()

    return cast(list[Point2D], convex_hull)
