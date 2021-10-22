from typing import Iterable, Union, cast

from cadquery import Workplane, Shape, Edge, Face, Shell, Solid, Wire, Compound

from .polyhedron import hull

from .cq_typing import T, FaceIndices, VectorLike, MeshGrid
from .util import toTuples, toVectors
from .curve import parametricEquation, circle

from OCP.BRepOffset import BRepOffset_MakeOffset, BRepOffset_Skin # type: ignore
from OCP.GeomAbs import GeomAbs_Intersection # type: ignore

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


def rotateExtrude(workplane: Workplane, radius: float, angle: float) -> Compound:
    circlePath = (Workplane(workplane.plane)
                    .parametricCurve(
                        parametricEquation(circle, radius = radius),
                        N = 96, 
                        stop = angle / 360
                    )
                 )

    xDir = workplane.plane.xDir.normalized()
    toExtruded = workplane.rotate(workplane.plane.origin, workplane.plane.origin + xDir, 90).translate(xDir * radius)
    rotateExtruded = (
        Workplane(workplane.plane)
            .add(toExtruded)
            .toPending()
            .sweep(circlePath)
            .val()
    )

    return cast(Compound, rotateExtruded)


def splineApproxSurface(points: MeshGrid, thickness: float) -> Union[Solid, Face]:    
    face = Face.makeSplineApprox([toVectors(col) for col in points])

    # THICKEN SURFACE
    # abs() because negative values are allowed to set direction of thickening
    if abs(thickness) > 0: 
        solid = BRepOffset_MakeOffset()
        solid.Initialize(
            face.wrapped,
            thickness,
            1.0e-5,
            BRepOffset_Skin,
            False,
            False,
            GeomAbs_Intersection,
            True,
        )  # The last True is important to make solid
        solid.MakeOffsetShape()
        return Solid(solid.Shape())
    else:
        return face