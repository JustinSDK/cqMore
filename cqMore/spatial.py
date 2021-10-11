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

        return (
            vtIndices,
            # faces 
            [
                (v1, v0, v2),
                (v0, v1, v3),
                (v1, v2, v3),
                (v2, v0, v3)
            ] 
            if n.dot(e) > 0 else 
            [
                (v0, v1, v2),
                (v1, v0, v3),
                (v2, v1, v3),
                (v0, v2, v3)
            ]
        )

    def _faceType(vectors, v, faces):
        vt0 = vectors[faces[0]]
        vt1 = vectors[faces[1]]
        vt2 = vectors[faces[2]]

        n = (vt1 - vt0).cross(vt2 - vt0)
        d = (vt0 - v).dot(n)

        return  1 if d > 0 else ( # convex
               -1 if d < 0 else   # concav
                0                 # coplane
        )

    def _nextFaces(i, currentFaces, types, edges):
        faces = [face for j, face in enumerate(currentFaces) if types[j] >= 0]

        for v0, v1, v2 in currentFaces:
            if edges[v0][v1] < 0 and edges[v0][v1] != edges[v1][v0]:
                faces.append((v0, v1, i))
        
            if edges[v1][v2] < 0 and edges[v1][v2] != edges[v2][v1]:
                faces.append((v1, v2, i))

            if edges[v2][v0] < 0 and edges[v2][v0] != edges[v0][v2]:
                faces.append((v2, v0, i))
        
        return faces

    vectors = [Vector(*p) for p in sorted(toTuples(points))]

    leng_vectors = len(vectors)
    edges = [[0] * leng_vectors for _ in range(leng_vectors)]
    
    vtIndices, faces = _fstTetrahedron(vectors)
    for i in range(leng_vectors):
        if not (i in vtIndices):
            types = [_faceType(vectors, vectors[i], face) for face in faces]
            for j in range(len(faces)):
                edges[faces[j][0]][faces[j][1]] = types[j]
                edges[faces[j][1]][faces[j][2]] = types[j]
                edges[faces[j][2]][faces[j][0]] = types[j]
            faces = _nextFaces(i, faces, types, edges)

    convex_vtIndices = {i for face in faces for i in face}
    convex_vertices = [vectors[i].toTuple() for i in convex_vtIndices]
    v_i_lookup = {v: i for i, v in enumerate(convex_vertices)}
    convex_faces = [
        tuple(v_i_lookup[convex_vertices[i]] for i in face)
        for face in faces
    ]

    return Polyhedron(convex_vertices, convex_faces)
