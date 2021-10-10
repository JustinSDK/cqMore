from cadquery import (
    Vector, 
    Edge, 
    Wire, 
    Solid, 
    Shell, 
    Face,
    Workplane
)

from typing import (
    Iterable
)

from .cq_typing import (
    VectorLike,
    FaceIndices,
    MeshGrid
)

from .util import toVectors

from math import radians, cos, sin

def polyhedron(points: Iterable[VectorLike], faces: Iterable[FaceIndices]) -> Solid:
    def _edges(vectors, face_indices):
        leng_vertices = len(face_indices)   
        return (
            Edge.makeLine(
                vectors[face_indices[i]], 
                vectors[face_indices[(i + 1) % leng_vertices]]
            ) 
            for i in range(leng_vertices)
        )

    vectors = toVectors(points)

    return Solid.makeSolid(
        Shell.makeShell(
            Face.makeFromWires(
                Wire.assembleEdges(
                    _edges(vectors, face_indices)
                )
            )
            for face_indices in faces
        )
    )

def surface(points: MeshGrid, thickness: float) -> Solid:
    leng_row = len(points)
    leng_col = len(points[0])
    leng_pts = leng_col * leng_row

    def _all_pts():
        face = Face.makeSplineApprox([[
                        Vector(*points[ri][ci]) 
                for ri in range(leng_row)
            ] for ci in range(leng_col)]
        )

        if thickness == 0:
            front_thicken_pts = [] 
            for row in points:
                for vt in toVectors(row):
                    front_thicken_pts.append([vt.x, vt.y, vt.z])
            return front_thicken_pts

        half_thickness = thickness / 2
        front_thicken_pts = [] 
        back_thicken_pts = [] 
        for row in points:
            for vt in toVectors(row):
                n = face.normalAt(vt).normalized()
                v = vt + n.multiply(half_thickness)
                front_thicken_pts.append([v.x, v.y, v.z])
                v = vt + n.multiply(-half_thickness)
                back_thicken_pts.append([v.x, v.y, v.z])
        return front_thicken_pts + back_thicken_pts

    def _all_faces():
        front_faces = []
        for ri in range(leng_row - 1):
            for ci in range(leng_col - 1):
                front_faces.append([ci + leng_col * ri, (ci + 1) + leng_col * ri, (ci + 1) + leng_col * (ri + 1)])
                front_faces.append([ci + leng_col * ri, (ci + 1) + leng_col * (ri + 1), ci + leng_col * (ri + 1)])

        if thickness == 0:
            return front_faces

        back_faces = [[f[2] + leng_pts, f[1] + leng_pts, f[0] + leng_pts] for f in front_faces]

        side_faces1 = []
        for ci in range(leng_col - 1):
            side_faces1.append([ci, ci + leng_pts, ci + 1])
            side_faces1.append([ci + leng_pts, ci + leng_pts + 1, ci + 1])

        side_faces2 = []
        side_faces4 = []
        rx = leng_col - 1
        for ri in range(leng_row - 1):
            side_faces2.append([rx + (ri + 1) * leng_col + leng_pts, rx + (ri + 1) * leng_col, rx + ri * leng_col])
            side_faces2.append([rx + ri * leng_row + leng_pts, rx + (ri + 1) * leng_col + leng_pts, rx + ri * leng_col])

            side_faces4.append([ri * leng_col, (ri + 1) * leng_col, (ri + 1) * leng_col + leng_pts])
            side_faces4.append([ri * leng_col, (ri + 1) * leng_col + leng_pts, ri * leng_row + leng_pts])

        side_faces3 = []
        for ci in range(leng_pts - leng_col, leng_pts - 1):
            side_faces3.append([ci + 1, ci + leng_pts, ci])
            side_faces3.append([ci + 1, ci + leng_pts + 1, ci + leng_pts])

        return front_faces + back_faces + side_faces1 + side_faces2 + side_faces3 + side_faces4

    return polyhedron(_all_pts(), _all_faces())

def uvsphere(radius, n: int = 2) -> Solid:
    angleStep = 180.0 / n
    vectors = []
    for p in range(n - 1, 0, -1):
        for t in range(2 * n):
            phi = radians(p * angleStep)
            theta = radians(t * angleStep)
            sinPhi = sin(phi)
            x = radius * sinPhi * cos(theta)
            y = radius * sinPhi * sin(theta)
            z = radius * cos(phi)
            vectors.append(Vector(x, y, z))
    vectors.append(Vector(0, 0, -radius))
    vectors.append(Vector(0, 0, radius))

    # ring
    leng_t = 2 * n
    faces = []
    for p in range(n - 2):
        for t in range(2 * n - 1):
            faces.append((t + leng_t * p, (t + 1) + leng_t * p, (t + 1) + leng_t * (p + 1)))
            faces.append((t + leng_t * p, (t + 1) + leng_t * (p + 1), t + leng_t * (p + 1)))
        t = 2 * n - 1
        faces.append((t + leng_t * p, leng_t * p, leng_t * (p + 1)))
        faces.append((t + leng_t * p, leng_t * (p + 1), t + leng_t * (p + 1)))
    
    # bottom
    leng_vectors = len(vectors)
    bi = leng_vectors - 2
    for t in range(2 * n - 1):
        faces.append((bi, t + 1, t))
    faces.append((bi, 0, 2 * n - 1))

    # top
    ti = leng_vectors - 1
    li = (n - 2) * leng_t
    for t in range(2 * n - 1):
        faces.append((ti, li + t, li + t + 1))
    faces.append((ti, li + (2 * n - 1), li))    

    return polyhedron(vectors, faces)