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

    - `radius`: sphere radius.
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


def tetrahedron(radius: float, detail: int = 0) -> Polyhedron:
    '''
    Create a tetrahedron.

    ## Parameters

    - `radius`: radius of the tetrahedron.
    - `detail`: setting this to a value greater than 0 adds vertices making it no longer a tetrahedron.

    ## Examples 

        from cqmore.polyhedron import tetrahedron
        from cqmore import Workplane

        radius = 1
        polyhedra = Workplane()
        for detail in range(5):
            polyhedra.add(
                Workplane()
                    .polyhedron(*tetrahedron(radius, detail))
                    .translate((2 * radius * detail, 0, 0))
            )

    '''

    vectors = [
        Vector(1, 1, 1), Vector(-1, -1, 1), Vector(-1, 1, -1), Vector(1, -1, -1)
    ]
    faces = [
        (2, 1, 0), (0, 3, 2), (1, 3, 0), (2, 3, 1)
    ]
    return _divide_project(vectors, faces, radius, detail)


def hexahedron(radius: float, detail: int = 0) -> Polyhedron:
    '''
    Create a hexahedron.

    ## Parameters

    - `radius`: radius of the hexahedron.
    - `detail`: setting this to a value greater than 0 adds vertices making it no longer a hexahedron.

    ## Examples 

        from cqmore.polyhedron import hexahedron
        from cqmore import Workplane

        radius = 1
        polyhedra = Workplane()
        for detail in range(5):
            polyhedra.add(
                Workplane()
                    .polyhedron(*hexahedron(radius, detail))
                    .translate((2 * radius * detail, 0, 0))
            )

    '''

    t = 1 / (3 ** 0.5)
    vectors = [
        Vector(t, t, t), Vector(-t, t, t), Vector(-t, -t, t), Vector(t, -t, t),
        Vector(t, t, -t), Vector(-t, t, -t), Vector(-t, -t, -t), Vector(t, -t, -t)
    ]
    faces = [
        (3, 7, 0), (7, 4, 0), 
        (0, 4, 1), (4, 5, 1),
        (5, 6, 2), (1, 5, 2),
        (6, 7, 3), (2, 6, 3),
        (2, 3, 0), (1, 2, 0),
        (7, 6, 5), (4, 7, 5)
    ]
    return _divide_project(vectors, faces, radius, detail)


def octahedron(radius: float, detail: int = 0) -> Polyhedron:
    '''
    Create a octahedron.

    ## Parameters

    - `radius`: radius of the octahedron.
    - `detail`: setting this to a value greater than 0 adds vertices making it no longer a octahedron.

    ## Examples 

        from cqmore.polyhedron import octahedron
        from cqmore import Workplane

        radius = 1
        polyhedra = Workplane()
        for detail in range(5):
            polyhedra.add(
                Workplane()
                    .polyhedron(*octahedron(radius, detail))
                    .translate((2 * radius * detail, 0, 0))
            )

    '''

    vectors = [
        Vector(1, 0, 0), Vector(-1, 0, 0), Vector(0, 1, 0), 
        Vector(0, -1, 0), Vector(0, 0, 1), Vector(0, 0, -1)
    ]
    faces = [
        (0, 2, 4), (0, 4, 3),	(0, 3, 5),
		(0, 5, 2), (1, 2, 5),	(1, 5, 3),
		(1, 3, 4), (1, 4, 2)
    ]
    return _divide_project(vectors, faces, radius, detail)


def dodecahedron(radius: float, detail: int = 0) -> Polyhedron:
    '''
    Create a dodecahedron.

    ## Parameters

    - `radius`: radius of the dodecahedron.
    - `detail`: setting this to a value greater than 0 adds vertices making it no longer a dodecahedron.

    ## Examples 

        from cqmore.polyhedron import dodecahedron
        from cqmore import Workplane

        radius = 1
        polyhedra = Workplane()
        for detail in range(5):
            polyhedra.add(
                Workplane()
                    .polyhedron(*dodecahedron(radius, detail))
                    .translate((2 * radius * detail, 0, 0))
            )

    '''

    t = (1 + 5 ** 0.5) / 2
    r = 1 / t
    vectors = [
			# (±1, ±1, ±1)
			Vector(-1, -1, -1), Vector(-1, -1, 1),
			Vector(-1, 1, -1), Vector(-1, 1, 1),
			Vector(1, -1, -1), Vector(1, -1, 1),
			Vector(1, 1, -1), Vector(1, 1, 1),

			# (0, ±1/φ, ±φ)
			Vector(0, -r, -t), Vector(0, -r, t),
			Vector(0, r, -t), Vector(0, r, t),

			# (±1/φ, ±φ, 0)
			Vector(-r, -t, 0), Vector(-r, t, 0),
			Vector(r, -t, 0), Vector(r, t, 0),

			# (±φ, 0, ±1/φ)
			Vector(-t, 0, -r), Vector(t, 0, -r),
			Vector(-t, 0, r), Vector(t, 0, r)
    ]
    faces = [
        (3, 11, 7), (3, 7, 15), (3, 15, 13),
        (7, 19, 17), (7, 17, 6), (7, 6, 15),
        (17, 4, 8), (17, 8, 10), (17, 10, 6),
        (8, 0, 16), (8, 16, 2), (8, 2, 10),
        (0, 12, 1), (0, 1, 18), (0, 18, 16),
        (6, 10, 2), (6, 2, 13), (6, 13, 15),
        (2, 16, 18), (2, 18, 3), (2, 3, 13),
        (18, 1, 9), (18, 9, 11), (18, 11, 3),
        (4, 14, 12), (4, 12, 0), (4, 0, 8),
        (11, 9, 5), (11, 5, 19), (11, 19, 7),
        (19, 5, 14), (19, 14, 4), (19, 4, 17),
        (1, 12, 14), (1, 14, 5), (1, 5, 9)
    ]
    return _divide_project(vectors, faces, radius, detail)


def icosahedron(radius: float, detail: int = 0) -> Polyhedron:
    '''
    Create a icosahedron.

    ## Parameters

    - `radius`: radius of the icosahedron.
    - `detail`: setting this to a value greater than 0 adds vertices making it no longer a icosahedron.

    ## Examples 

        from cqmore.polyhedron import icosahedron
        from cqmore import Workplane

        radius = 1
        polyhedra = Workplane()
        for detail in range(5):
            polyhedra.add(
                Workplane()
                    .polyhedron(*icosahedron(radius, detail))
                    .translate((2 * radius * detail, 0, 0))
            )

    '''

    t = (1 + 5 ** 0.5) / 2
    vectors = [
        Vector(-1, t, 0), Vector(1, t, 0), Vector(- 1, -t, 0), Vector(1, -t, 0),
        Vector(0, -1, t), Vector(0, 1, t), Vector(0, -1, -t),  Vector(0, 1, -t),
        Vector(t, 0, -1), Vector(t, 0, 1), Vector(-t, 0, -1),  Vector(-t, 0, 1)
    ]
    faces = [
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2),	(10, 7, 6),	(7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),	(3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
    ]
    return _divide_project(vectors, faces, radius, detail)


def _divide_project(vectors, faces, radius, detail):
    def _idx(ci, ri, ri_base):
        return ci + ri_base[ri]

    def _divide(vectors, detail):
        rows = detail + 1
        vc =  vectors[1] - vectors[0]
        vr = vectors[2] - vectors[0]
        dc = vc / rows
        dr = vr / rows
        vts = [
            vectors[0] + ci * dc + ri * dr
            for ri in range(0, rows + 1)
                for ci in range(0, rows - ri + 1)
        ]

        acc = 0
        ri_base = []
        for ri in range(rows + 1):
            ri_base.append(acc)
            acc = acc + rows - ri + 1

        faces = []
        for ri in range(rows):
            cols = rows - ri - 1
            for ci in range(rows - ri):
                faces.append([
                    _idx(ci, ri, ri_base),
                    _idx(ci + 1, ri, ri_base),
                    _idx(ci, ri + 1, ri_base)
                ])
                if ci != cols:
                    faces.append([
                        _idx(ci + 1, ri, ri_base),
                        _idx(ci + 1, ri + 1, ri_base),
                        _idx(ci, ri + 1, ri_base)
                    ])

        return (vts, faces)

    if detail == 0:
        return Polyhedron(
            [(vt / vt.Length * radius).toTuple() for vt in vectors],
            faces
        )

    subdivided_all = []
    for face in faces:
        subdivided_all.append(
            _divide([vectors[i] for i in face], detail)
        )

    flatten_points = [
        (vt / vt.Length * radius).toTuple()
        for vts, _ in subdivided_all
            for vt in vts
    ]
    
    pts_number_per_tri = len(subdivided_all[0][0])
    flatten_faces = [
        (face[0] + i * pts_number_per_tri, face[1] + i * pts_number_per_tri, face[2] + i * pts_number_per_tri)
        for i in range(len(subdivided_all))
            for face in subdivided_all[i][1]
    ]

    return Polyhedron(flatten_points, flatten_faces)
    

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

    def _append_face_normals(ci, ri, vectors, vt_normal_lt):
        v0 = vectors[ri][ci]
        v1 = vectors[ri][ci + 1]
        v2 = vectors[ri + 1][ci + 1]

        vt_normal_lt[ri][ci].append((v1 - v0).cross(v2 - v0))
        vt_normal_lt[ri][ci + 1].append((v2 - v1).cross(v0 - v1))
        vt_normal_lt[ri + 1][ci + 1].append((v0 - v2).cross(v1 - v2))

        v0 = vectors[ri][ci]
        v1 = vectors[ri + 1][ci + 1]
        v2 = vectors[ri + 1][ci]

        vt_normal_lt[ri][ci].append((v1 - v0).cross(v2 - v0))
        vt_normal_lt[ri + 1][ci + 1].append((v2 - v1).cross(v0 - v1))
        vt_normal_lt[ri + 1][ci].append((v0 - v2).cross(v1 - v2))

    def _all_pts():
        vectors = [toVectors(row) for row in points]

        if thickness == 0:
            front_thicken_pts = [] 
            for row in vectors:
                for vt in row:
                    front_thicken_pts.append([vt.x, vt.y, vt.z])
            return front_thicken_pts

        vt_normal_lt = [[[] for _ in range(leng_col)] for _ in range(leng_row)]
        for ri in range(leng_row - 1):
            for ci in range(leng_col - 1):
                _append_face_normals(ci, ri, vectors, vt_normal_lt)

        half_thickness = thickness / 2
        front_thicken_pts = [] 
        back_thicken_pts = [] 

        for ri in range(leng_row):
            for ci in range(leng_col):
                # vertex normal
                n = sum(vt_normal_lt[ri][ci], Vector()).normalized()
                vt = vectors[ri][ci]
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
            side_faces2.append([rx + ri * leng_col + leng_pts, rx + (ri + 1) * leng_col + leng_pts, rx + ri * leng_col])

            side_faces4.append([ri * leng_col, (ri + 1) * leng_col, (ri + 1) * leng_col + leng_pts])
            side_faces4.append([ri * leng_col, (ri + 1) * leng_col + leng_pts, ri * leng_col + leng_pts])

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

