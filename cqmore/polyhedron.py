"""
Provide the `Polyhedron` class and functions for creating `Polyhedron` instances. 
The `Polyhedron` class defines `points` and `faces` attributes. Here is a way 
to use them.

    from cqmore.polyhedron import uvSphere
    from cqmore import Workplane

    sphere = (Workplane()
                .polyhedron(*uvSphere(radius = 10, widthSegments = 10, heightSegments = 5))
             )

"""

from math import cos, radians, sin, pi, tau

from typing import Iterable, NamedTuple, Union, cast

from cadquery import Vector
from cadquery.cq import T, VectorLike

from ._util import toTuples
from ._typing import MeshGrid, Point3D, FaceIndices

import numpy


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


def uvSphere(radius: float, widthSegments: int = 3, heightSegments: int = 2) -> Polyhedron:
    '''
    Create a UV sphere.

    ## Parameters

    - `radius`: sphere radius.
    - `widthSegments`: number of horizontal segments.
    - `heightSegments`: number of vertical segments.

    ## Examples 

        from cqmore.polyhedron import uvSphere
        from cqmore import Workplane

        sphere = (Workplane()
                    .polyhedron(*uvSphere(radius = 10, widthSegments = 10, heightSegments = 5))
                 )

    '''

    thetaStep = tau / widthSegments
    phiStep = pi / heightSegments
    points = []
    for p in range(heightSegments - 1, 0, -1):
        for t in range(widthSegments):
            phi = p * phiStep
            theta = t * thetaStep
            sinPhi = sin(phi)
            x = radius * sinPhi * cos(theta)
            y = radius * sinPhi * sin(theta)
            z = radius * cos(phi)
            points.append((x, y, z))
    points.extend(((0, 0, -radius), (0, 0, radius)))

    # ring
    faces = []
    p_stop = heightSegments - 2
    t_stop = widthSegments - 1
    for p in range(p_stop):
        for t in range(t_stop):
            i0 = t + widthSegments * p
            i1 = (t + 1) + widthSegments * p
            i2 = (t + 1) + widthSegments * (p + 1)
            i3 = t + widthSegments * (p + 1)
            faces.extend(((i0, i1, i2), (i0, i2, i3)))
        i0 = t_stop + widthSegments * p
        i1 = widthSegments * p
        i2 = widthSegments * (p + 1)
        i3 = t_stop + widthSegments * (p + 1)
        faces.extend(((i0, i1, i2), (i0, i2, i3)))
    
    # bottom
    leng_points = len(points)
    bi = leng_points - 2
    for t in range(t_stop):
        faces.append((bi, t + 1, t))
    faces.append((bi, 0, t_stop))

    # top
    ti = leng_points - 1
    li = p_stop * widthSegments
    for t in range(t_stop):
        faces.append((ti, li + t, li + t + 1))
    faces.append((ti, li + t_stop, li))    

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

    vectors = (
        Vector(1, 1, 1), Vector(-1, -1, 1), Vector(-1, 1, -1), Vector(1, -1, -1)
    )
    faces = (
        (2, 1, 0), (0, 3, 2), (1, 3, 0), (2, 3, 1)
    )
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
    vectors = (
        Vector(t, t, t), Vector(-t, t, t), Vector(-t, -t, t), Vector(t, -t, t),
        Vector(t, t, -t), Vector(-t, t, -t), Vector(-t, -t, -t), Vector(t, -t, -t)
    )
    faces = (
        (3, 7, 0), (7, 4, 0), 
        (0, 4, 1), (4, 5, 1),
        (5, 6, 2), (1, 5, 2),
        (6, 7, 3), (2, 6, 3),
        (2, 3, 0), (1, 2, 0),
        (7, 6, 5), (4, 7, 5)
    )
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

    vectors = (
        Vector(1, 0, 0), Vector(-1, 0, 0), Vector(0, 1, 0), 
        Vector(0, -1, 0), Vector(0, 0, 1), Vector(0, 0, -1)
    )
    faces = (
        (0, 2, 4), (0, 4, 3),    (0, 3, 5),
        (0, 5, 2), (1, 2, 5),    (1, 5, 3),
        (1, 3, 4), (1, 4, 2)
    )
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
    vectors = (
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
    )
    faces = (
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
    )
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
    vectors = (
        Vector(-1, t, 0), Vector(1, t, 0), Vector(- 1, -t, 0), Vector(1, -t, 0),
        Vector(0, -1, t), Vector(0, 1, t), Vector(0, -1, -t),  Vector(0, 1, -t),
        Vector(t, 0, -1), Vector(t, 0, 1), Vector(-t, 0, -1),  Vector(-t, 0, 1)
    )
    faces = (
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2),    (10, 7, 6),    (7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),    (3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
    )
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
        vts = tuple(
            vectors[0] + ci * dc + ri * dr
            for ri in range(0, rows + 1)
                for ci in range(0, rows - ri + 1)
        )

        acc = 0
        ri_base = []
        for ri in range(rows + 1):
            ri_base.append(acc)
            acc = acc + rows - ri + 1

        faces = []
        for ri in range(rows):
            cols = rows - ri - 1
            for ci in range(rows - ri):
                faces.append((
                    _idx(ci, ri, ri_base),
                    _idx(ci + 1, ri, ri_base),
                    _idx(ci, ri + 1, ri_base)
                ))
                if ci != cols:
                    faces.append((
                        _idx(ci + 1, ri, ri_base),
                        _idx(ci + 1, ri + 1, ri_base),
                        _idx(ci, ri + 1, ri_base)
                    ))

        return (vts, faces)

    if detail == 0:
        return Polyhedron(
            tuple((vt / vt.Length * radius).toTuple() for vt in vectors),
            faces
        )

    subdivided_all = []
    for face in faces:
        subdivided_all.append(
            _divide([vectors[i] for i in face], detail)
        )

    flatten_points = tuple(
        (vt / vt.Length * radius).toTuple()
        for vts, _ in subdivided_all
            for vt in vts
    )
    
    pts_number_per_tri = len(subdivided_all[0][0])
    flatten_faces = tuple(
        (face[0] + i * pts_number_per_tri, face[1] + i * pts_number_per_tri, face[2] + i * pts_number_per_tri)
        for i in range(len(subdivided_all))
            for face in subdivided_all[i][1]
    )

    return Polyhedron(flatten_points, flatten_faces)
    

def star(outerRadius: float = 1, innerRadius: float =  0.381966, height: float = 0.5, n: int = 5) -> Polyhedron:
    """
    Create a star.

    ## Parameters

    - `outerRadius`: the outer radius of the star. 
    - `innerRadius`: the inner radius of the star.
    - `height`: the star height.
    - `n`: the burst number.

    ## Examples 

        from cqmore import Workplane
        from cqmore.polyhedron import star

        polyhedron = Workplane().polyhedron(*star()) 

    """

    right = tau / 4
    thetaStep = tau / n
    half_thetaStep = thetaStep / 2
    points = []
    for i in range(n):
        a = thetaStep * i + right
        outerPoint = (outerRadius * cos(a), outerRadius * sin(a), 0)
        innerPoint = (innerRadius * cos(a + half_thetaStep), innerRadius * sin(a + half_thetaStep), 0)
        points.extend((outerPoint, innerPoint)) 
    
    half_height = height / 2
    points.extend(((0, 0, half_height), (0, 0, -half_height)))

    leng_star = n * 2
    
    faces = []
    for i in range(leng_star):
        j = (i + 1) % leng_star
        faces.extend(((i, j, leng_star), (leng_star + 1, j, i)))

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
            for y in range(min_value, max_value, step)
        ] for x in range(min_value, max_value, step)]

        sf = Workplane().polyhedron(*gridSurface(points, thickness))

    """

    # transpose and creater vectors
    if isinstance(points[0][0], Vector):
        vectors = cast(tuple[tuple[Vector]],
            tuple(
                tuple(points[ci][ri] for ci in range(len(points))) for ri in range(len(points[0]))
            )
        )
    else:
        vectors = cast(tuple[tuple[Vector]],
            tuple(
                tuple(Vector(*points[ci][ri]) for ci in range(len(points))) for ri in range(len(points[0]))
            )
        )

    leng_row = len(vectors)
    leng_col = len(vectors[0])
    leng_pts = leng_col * leng_row

    def _append_face_normals(ci, ri, vt_normal_lt):
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
        if thickness == 0:
            return tuple((vt.x, vt.y, vt.z) for row in vectors for vt in row)

        vt_normal_lt = [[[] for _ in range(leng_col)] for _ in range(leng_row)]
        for ri in range(leng_row - 1):
            for ci in range(leng_col - 1):
                _append_face_normals(ci, ri, vt_normal_lt)

        half_thickness = thickness / 2
        front_thicken_pts = [] 
        back_thicken_pts = [] 

        for ri in range(leng_row):
            for ci in range(leng_col):
                # vertex normal
                n = sum(vt_normal_lt[ri][ci], Vector()).normalized()
                vt = vectors[ri][ci]
                v = vt + n.multiply(half_thickness)
                front_thicken_pts.append((v.x, v.y, v.z))
                v = vt + n.multiply(-half_thickness)
                back_thicken_pts.append((v.x, v.y, v.z))

        return front_thicken_pts + back_thicken_pts

    def _all_faces():
        faces = []
        for ci in range(leng_col - 1):
            i0 = ci
            i1 = (ci + 1)
            i2 = (ci + 1) + leng_col 
            i3 = ci + leng_col
            faces.extend(((i0, i1, i2), (i0, i2, i3)))

        row0 = numpy.array(faces)
        for ri in range(1, leng_row - 1):
            faces.extend(map(tuple, (row0 + ri * leng_col)))

        if thickness == 0:
            return faces

        # fack faces
        faces.extend(tuple((f[2] + leng_pts, f[1] + leng_pts, f[0] + leng_pts) for f in faces))

        # side faces #1
        for ci in range(leng_col - 1):
            i1 = ci + leng_pts
            i2 = ci + 1
            i3 = ci + leng_pts + 1
            faces.extend(((ci, i1, i2), (i1, i3, i2)))

        # side faces #2 #4
        rx = leng_col - 1
        for ri in range(leng_row - 1):
            i0 = rx + (ri + 1) * leng_col + leng_pts
            i1 = rx + (ri + 1) * leng_col
            i2 = rx + ri * leng_col
            i3 = rx + ri * leng_col + leng_pts
            faces.extend(((i0, i1, i2), (i3, i0, i2)))

            i0 = ri * leng_col
            i1 = (ri + 1) * leng_col
            i2 = (ri + 1) * leng_col + leng_pts
            i3 = ri * leng_col + leng_pts
            faces.extend(((i0, i1, i2), (i0, i2, i3)))

        # side faces #3
        for ci in range(leng_pts - leng_col, leng_pts - 1):
            i0 = ci + 1
            i1 = ci + leng_pts
            i2 = ci + leng_pts + 1
            faces.extend(((i0, i1, ci), (i0, i2, i1)))

        return faces

    return Polyhedron(_all_pts(), _all_faces())


def hull(points: Iterable[VectorLike]) -> Polyhedron:
    """
    Create a convex hull through the provided points. 

    ## Parameters

    - `points`: a list of 3D points. 

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
            (
                (v1, v0, v2),
                (v0, v1, v3),
                (v1, v2, v3),
                (v2, v0, v3)
            )
            if n.dot(e) > 0 else 
            (
                (v0, v1, v2),
                (v1, v0, v3),
                (v2, v1, v3),
                (v0, v2, v3)
            )
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

    vectors = tuple(Vector(*p) for p in sorted(toTuples(points)))

    leng_vectors = len(vectors)
    edges = [[0] * leng_vectors for _ in range(leng_vectors)]
    
    vtIndices, faces = _fstTetrahedron(vectors)
    for i in range(leng_vectors):
        if not (i in vtIndices):
            types = tuple(_faceType(vectors, vectors[i], face) for face in faces)
            for j in range(len(faces)):
                edges[faces[j][0]][faces[j][1]] = types[j]
                edges[faces[j][1]][faces[j][2]] = types[j]
                edges[faces[j][2]][faces[j][0]] = types[j]
            faces = _nextFaces(i, faces, types, edges)

    pts = tuple(v.toTuple() for v in vectors)
    convex_vtIndices = {i for face in faces for i in face}
    convex_vertices = tuple(pts[i] for i in convex_vtIndices)

    v_i_lookup = {v: i for i, v in enumerate(convex_vertices)}
    convex_faces = tuple(
        tuple(v_i_lookup[pts[i]] for i in face)
        for face in faces
    )

    return Polyhedron(convex_vertices, convex_faces)


def superellipsoid(e: float, n: float, widthSegments: int = 3, heightSegments: int = 2) -> Polyhedron:
    """
    Create a [superellipsoid](https://en.wikipedia.org/wiki/Superellipsoid).

    ## Parameters

    - `e`: the east-west parameter.
    - `n`: the north-south parameter.
    - `widthSegments`: number of horizontal segments.
    - `heightSegments`: number of vertical segments.

    ## Examples 

        from cqmore import Workplane
        from cqmore.polyhedron import superellipsoid

        r = Workplane().polyhedron(*superellipsoid(2.5, .25, widthSegments = 24, heightSegments = 12))

    """

    # Signum function
    def _sgn(n):
        return n and (1, -1)[n < 0]
    
    def _c(w, m):
        cosw = cos(w)
        return _sgn(cosw) * pow(abs(cosw), m)

    def _s(w, m):
        sinw = sin(w)
        return _sgn(sinw) * pow(abs(sinw), m)

    a = 1
    b = 1
    c = 1

    real_nPhi = heightSegments + 2
    thetaStep = tau / widthSegments
    phiStep = pi / real_nPhi
    sections = []
    for p in range(1, real_nPhi):
        phi = -pi / 2 + p * phiStep
        section = []
        for t in range(widthSegments):
            theta = t * thetaStep
            x = a * _c(phi, n) * _c(theta, e)
            y = b * _c(phi, n) * _s(theta, e)
            z = c * _s(phi, n)
            section.append((x, y, z))
        sections.append(section)
    
    return sweep(sections)


def polarZonohedra(n: int, theta: float = 35.5) -> Polyhedron:
    """
    Create a polar zonohedra.

    ## Parameters

    - `n`: n equal rhombs surrounding one vertex. (rotational symmetry).
    - `theta `: the pitch angle of the edges.

    ## Examples 

        from cqmore.polyhedron import polarZonohedra
        from cqmore import Workplane

        pz = Workplane().polyhedron(*polarZonohedra(8, 45))

    """    
    def _vertex(i, j, n, theta):
        if i > j:
            return (0, 0, 0)
        
        x = 0
        y = 0
        z = 0
        for k in range(i, j + 1):
            rtheta = radians(theta)
            cosa = cos(rtheta)
            a_i_n = radians(360 * k / n)
            x += cosa * cos(a_i_n)
            y += cosa * sin(a_i_n)
            z += sin(rtheta)
        return (x, y, z)

    def _rhombi(i, j, n, theta):
        return [
            _vertex(i, -1 + j, n, theta),
            _vertex(i + 1, -1 + j, n, theta),
            _vertex(i + 1, j, n, theta),
            _vertex(i, j, n, theta)
        ]

    vt_faces = (_rhombi(i, j, n, theta) for i in range(n) for j in range(i + 1, n + i))
    points = [vt for face_vts in vt_faces for vt in face_vts]
    faces = [tuple(i * 4 + j for j in range(4)) for i in range(int(len(points) / 4))]
    
    return Polyhedron(points, faces)
    

def sweep(profiles: Union[list[list[Point3D]], list[list[Vector]]], closeIdx: int = -1) -> Polyhedron:
    """
    Create a swept polyhedron.

    ## Parameters

    - `profiles`: list of profiles.
    - `closeIdx`: setting it to a value >= 0 creates faces between the first and last profile. 
                  The value decides which index of the last profile is connected to the first index 
                  of the first profile.

    ## Examples 

        # ex1

        from cqmore import Workplane
        from cqmore.polyhedron import sweep

        profiles = [
            [(10, 0, 0), (10, 0, 10), (20, 0, 10), (20, 0, 0)],
            [(0, 10, 0), (0, 10, 10), (0, 20, 10), (0, 20, 0)],
            [(-10, 0, 0), (-10, 0, 10), (-20, 0, 10), (-20, 0, 0)],
            [(0, -10, 0), (0, -10, 10), (0, -20, 10), (0, -20, 0)]
        ]

        r = Workplane().polyhedron(*sweep(profiles))

        # ex2

        from cqmore import Workplane
        from cqmore.polyhedron import sweep

        profiles = [
            [(10, 0, 0), (10, 0, 10), (20, 0, 10), (20, 0, 0)],
            [(0, 10, 0), (0, 10, 10), (0, 20, 10), (0, 20, 0)],
            [(-10, 0, 0), (-10, 0, 10), (-20, 0, 10), (-20, 0, 0)],
            [(0, -10, 0), (0, -10, 10), (0, -20, 10), (0, -20, 0)]
        ]

        r = Workplane().polyhedron(*sweep(profiles, closeIdx = 0))

    """

    def _revolving_faces0(leng_per_section):
        faces = []
        for i in range(leng_per_section):
            rbi = (i + 1) % leng_per_section
            lti = leng_per_section + i
            rti = leng_per_section + rbi
            faces.extend(((i, rbi, lti), (rbi, rti, lti)))
        return faces

    leng_sections = len(profiles)
    leng_per_section = len(profiles[0])

    faces0 = _revolving_faces0(leng_per_section)
    np_faces0 = numpy.array(faces0)

    faces = faces0
    for s in range(1, leng_sections - 1):
        faces.extend(map(tuple, (np_faces0 + (s * leng_per_section))))

    if closeIdx == -1:
        faces.extend((
            tuple(range(leng_per_section))[::-1],
            tuple(range(leng_per_section * (leng_sections - 1), leng_per_section * leng_sections))
        ))
    else:
        idx_base = leng_per_section * (leng_sections - 1)
        for i in range(leng_per_section):
            li0 = idx_base + (closeIdx + i) % leng_per_section
            li1 = idx_base + (closeIdx + i + 1) % leng_per_section
            fi1 = (i + 1) % leng_per_section
            faces.extend(((li0, li1, i), (li1, fi1, i)))

    points = tuple(p for section in profiles for p in toTuples(section))
    return Polyhedron(cast(Iterable[Point3D], points), faces)