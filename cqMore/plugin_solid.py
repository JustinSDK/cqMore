from typing import Iterable, Union, cast

from cadquery import Workplane, Shape, Edge, Face, Shell, Solid, Vector, Wire
from cadquery.occ_impl.shapes import Compound

from .polyhedron import hull

from .cq_typing import T, FaceIndices, MeshGrid, VectorLike
from .util import toTuples, toVectors

def makePolyhedron(points: Iterable[VectorLike], faces: Iterable[FaceIndices]) -> Solid:
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

    return makePolyhedron(_all_pts(), _all_faces())

def polylineJoin(points: Iterable[VectorLike], join: Union[T, Solid, Compound]) -> Union[Solid, Compound]:
    if isinstance(join, Workplane):
        joinSolidCompound = join.val()
    elif isinstance(join, Solid) or isinstance(join, Compound):
        joinSolidCompound = join
    else:
        raise ValueError("Join type '{}' is not allowed".format(type(join)))
    
    pts = toTuples(points)
    join_vts = [v.toTuple() for v in cast(Shape, joinSolidCompound).Vertices()]
    joins = [[(p[0] + vt[0], p[1] + vt[1], p[2] + vt[2]) for vt in join_vts] for p in pts]

    workplanes = [
        Workplane(makePolyhedron(*hull(joins[i] + joins[i + 1])))
        for i in range(len(pts) - 1)
    ]

    wp = workplanes[0]
    for i in range(1, len(workplanes)):
        wp = wp.union(workplanes[i])

    return cast(Union[Solid, Compound], wp.val())