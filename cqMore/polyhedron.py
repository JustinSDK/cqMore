"""
This module provides the `Polyhedron` class and functions for creating 
`Polyhedron` instances. The `Polyhedron` class defines `points` and 
`faces` attributes. Here is a way to use them.

    from cqmore.polyhedron import uvSphere
    from cqmore import Workplane

    sphere = (Workplane()
                .polyhedron(*uvSphere(radius = 10, rings = 5))
            )

"""

from math import cos, radians, sin

from typing import Iterable, NamedTuple
from .cq_typing import Point3D, FaceIndices

from cadquery import Vector

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
    vectors = []
    for p in range(rings - 1, 0, -1):
        for t in range(2 * rings):
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
    leng_vectors = len(vectors)
    bi = leng_vectors - 2
    for t in range(2 * rings - 1):
        faces.append((bi, t + 1, t))
    faces.append((bi, 0, 2 * rings - 1))

    # top
    ti = leng_vectors - 1
    li = (rings - 2) * leng_t
    for t in range(2 * rings - 1):
        faces.append((ti, li + t, li + t + 1))
    faces.append((ti, li + (2 * rings - 1), li))    

    return Polyhedron(vectors, faces)