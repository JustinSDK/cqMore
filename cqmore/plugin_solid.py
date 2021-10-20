from typing import Iterable, Union, cast

from cadquery import Plane, Workplane, Shape, Edge, Face, Shell, Solid, Wire, Compound

from .polyhedron import hull

from .cq_typing import T, FaceIndices, VectorLike
from .util import toTuples, toVectors
from .curve import parametricEquation, circle


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


def rotateExtrude(workplane: Workplane, radius: float, angle: float = 360) -> Compound:
    circlePath = workplane.parametricCurve(parametricEquation(circle, radius = radius), stop = angle / 360)

    xDir = workplane.plane.xDir.normalized()
    toExtruded = workplane.rotateAboutCenter(xDir, 90).translate(xDir * radius)
    rotateExtruded = (
        Workplane(Plane(origin = (0, 0, 0), normal = workplane.plane.zDir))
            .add(toExtruded)
            .toPending()
            .sweep(circlePath)
            .val()
    )

    return cast(Compound, rotateExtruded)