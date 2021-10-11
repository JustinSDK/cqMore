from typing import Iterable, cast

from cadquery import Vector

from .cq_typing import Point2D, VectorLike
from .polyhedron import Polyhedron
from .util import toTuples


def hull2D(points: Iterable[VectorLike]) -> list[Point2D]:
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
    
    return cast(list[Point2D], convex_hull)

def hull(points: Iterable[VectorLike]) -> Polyhedron:
    def _tv1(vectors, vtIndices):
        v0 = vtIndices[0]
        for v1 in range(1, len(vectors)):
            if (vectors[v1] - vectors[v0]).Length != 0:
                return v1
        raise ValueError('points are the same')
    
    def _tv2(vectors, vtIndices):
        v0, v1 = vtIndices
        for v2 in range(v1 + 1, len(vectors)):
            nL = (vectors[v1] - vectors[v0]).cross(vectors[v2] - vectors[v0]).Length
            if nL != 0:
                return v2
        raise ValueError('collinear points')
            
    def _tv3(vectors, vtIndices):
        v0, v1, v2 = vtIndices
        n = (vectors[v1] - vectors[v0]).cross(vectors[v2] - vectors[v0])
        for v3 in range(v2 + 1, len(vectors)):
            e = vectors[v3] - vectors[v0]
            if n.dot(e) != 0:
                return v3

        raise ValueError('coplanar points')

    def _fstTetrahedron(vectors):
        vtIndices = [0]
        vtIndices.append(_tv1(vectors, vtIndices))
        vtIndices.append(_tv2(vectors, vtIndices))
        vtIndices.append(_tv3(vectors, vtIndices))

        v0, v1, v2, v3 = vtIndices
        n = (vectors[v1] - vectors[v0]).cross(vectors[v2] - vectors[v0])
        e = vectors[v3] - vectors[v0]

        return {
            'vtIndices': vtIndices, 
            'faces': [
                        [v1, v0, v2],
                        [v0, v1, v3],
                        [v1, v2, v3],
                        [v2, v0, v3]
                     ] 
                     if n.dot(e) > 0 else 
                     [
                        [v0, v1, v2],
                        [v1, v0, v3],
                        [v2, v1, v3],
                        [v0, v2, v3]
                     ]
        }

    vectors = [Vector(*p) for p in sorted(toTuples(points))]
    edges = [[]] * len(vectors)


    return Polyhedron([], [])
