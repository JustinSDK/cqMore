"""
Provide the `Polyhedron` class and functions for creating `Polyhedron` instances. 
The `Polyhedron` class defines `points` and `faces` attributes. Here is a way 
to use them.

    from cqmore.polyhedron import uvSphere
    from cqmore import Workplane

    sphere = (Workplane()
                .polyhedron(*uvSphere(radius = 10, rings = 5))
            )

"""

from math import cos, radians, sin

from typing import Iterable, NamedTuple

from .util import toTuples, toVectors
from .cq_typing import MeshGrid, Point3D, FaceIndices, VectorLike
from cadquery import Vector, Face

class Polyhedron(NamedTuple):
    '''
    Define a polyhedron.

    ## Parameters

    - `points`: points of vertices. 
    - `faces`: face indices.

    ## Examples     

        from cqmore.polyhedron import Polyhedron
        from cqmore import Workplane

        points = (
            (5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5)
        )

        faces = (
            (0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3)
        )

        tetrahedron = Polyhedron(points, faces)
        tetrahedrons = (Workplane()
                        .rect(15, 15, forConstruction = True)
                        .vertices()
                        .polyhedron(*tetrahedron)
                    )   

    '''

    points: Iterable[Point3D]
    faces: Iterable[FaceIndices]

def uvSphere(radius: float, rings: int = 2) -> Polyhedron:
    '''
    Create a UV sphere.

    ## Parameters

    - `radius`: sphere radius
    - `rings`: number of horizontal segments.

    ## Examples 

        from cqmore.polyhedron import uvSphere
        from cqmore import Workplane

        sphere = (Workplane()
                    .polyhedron(*uvSphere(radius = 10, rings = 5))
                )

    '''

    angleStep = 180.0 / rings
    points = []
    for p in range(rings - 1, 0, -1):
        for t in range(2 * rings):
            phi = radians(p * angleStep)
            theta = radians(t * angleStep)
            sinPhi = sin(phi)
            x = radius * sinPhi * cos(theta)
            y = radius * sinPhi * sin(theta)
            z = radius * cos(phi)
            points.append((x, y, z))
    points.append((0, 0, -radius))
    points.append((0, 0, radius))

    # ring
    leng_t = 2 * rings
    faces = []
    for p in range(rings - 2):
        for t in range(2 * rings - 1):
            faces.append((t + leng_t * p, (t + 1) + leng_t * p, (t + 1) + leng_t * (p + 1)))
            faces.append((t + leng_t * p, (t + 1) + leng_t * (p + 1), t + leng_t * (p + 1)))
        t = 2 * rings - 1
        faces.append((t + leng_t * p, leng_t * p, leng_t * (p + 1)))
        faces.append((t + leng_t * p, leng_t * (p + 1), t + leng_t * (p + 1)))
    
    # bottom
    leng_points = len(points)
    bi = leng_points - 2
    for t in range(2 * rings - 1):
        faces.append((bi, t + 1, t))
    faces.append((bi, 0, 2 * rings - 1))

    # top
    ti = leng_points - 1
    li = (rings - 2) * leng_t
    for t in range(2 * rings - 1):
        faces.append((ti, li + t, li + t + 1))
    faces.append((ti, li + (2 * rings - 1), li))    

    return Polyhedron(points, faces)

def gridSurface(points: MeshGrid, thickness: float = 0) -> Polyhedron:
    """
    Create a surface with a coordinate meshgrid.

    ## Parameters

    - `points`: a coordinate meshgrid.
    - `thickness`: the amount of being thick (return 2D surface if 0).

    ## Examples 

        from math import sqrt, cos, radians
        from cqmore import Workplane
        from cqmore.polyhedron import gridSurface

        def ripple(x, y):
            n = radians(sqrt(x ** 2 + y ** 2))
            return (x, y, 30 * (cos(n) + cos(3 * n)))

        min_value = -200
        max_value = 200
        step = 10
        thickness = 5

        points = [[
                ripple(x, y) 
            for x in range(min_value, max_value, step)
        ] for y in range(min_value, max_value, step)]

        sf = Workplane().polyhedron(*gridSurface(points, thickness))

    """

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

    return Polyhedron(_all_pts(), _all_faces())

def hull(points: Iterable[VectorLike]) -> Polyhedron:
    """
    Create a convex hull through the provided points. 

    ## Parameters

    - `points`: a list of 3D points. If it's `None`, attempt to hull all of the items on the stack 
                to create a convex hull.

    ## Examples 

        from cqmore import Workplane
        from cqmore.polyhedron import hull

        points = (
            (50, 50, 50),
            (50, 50, 0),
            (-50, 50, 0),
            (-50, -50, 0),
            (50, -50, 0),
            (0, 0, 50),
            (0, 0, -50)
        )

        convex_hull = Workplane().polyhedron(*hull(points))

        """

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

    pts = [v.toTuple() for v in vectors]
    convex_vtIndices = {i for face in faces for i in face}
    convex_vertices = [pts[i] for i in convex_vtIndices]

    v_i_lookup = {v: i for i, v in enumerate(convex_vertices)}
    convex_faces = [
        tuple(v_i_lookup[pts[i]] for i in face)
        for face in faces
    ]

    return Polyhedron(convex_vertices, convex_faces)
