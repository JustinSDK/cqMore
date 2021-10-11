from typing import (
    Iterable,
    NamedTuple
)
from cqMore.cq_typing import (
    VectorLike,
    FaceIndices,
    MeshGrid
)

from cqMore.util import toVectors, toTuples

from cadquery import Vector

class Polyhedron(NamedTuple):
    points: Iterable[VectorLike]
    faces: Iterable[FaceIndices]

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

    print(_fstTetrahedron(vectors))

    return Polyhedron([], [])

hull((
    (50, 50, 50),
    (50, 50, 0),
    (-50, 50, 0),
    (-50, -50, 0),
    (50, -50, 0),
    (0, 0, 50),
    (0, 0, -50)
))
