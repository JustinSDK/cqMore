from typing import Iterable, Union, cast

from cadquery import Workplane, Shape, Edge, Face, Shell, Solid, Wire, Compound

from .polyhedron import hull

from ._typing import T, FaceIndices, VectorLike, MeshGrid
from ._util import toTuples, toVectors

from OCP.BRepOffset import BRepOffset_MakeOffset, BRepOffset_Skin # type: ignore
from OCP.GeomAbs import GeomAbs_Intersection # type: ignore

import numpy

def makePolyhedron(points: Iterable[VectorLike], faces: Iterable[FaceIndices]) -> Solid:
    vectors = numpy.array(toVectors(points))

    return Solid.makeSolid(
        Shell.makeShell(
            Face.makeFromWires(
                Wire.assembleEdges(
                    Edge.makeLine(*vts[[-1 + i, i]]) for i in range(vts.size)
                )
            )
            for vts in (vectors[face] for face in numpy.array(faces))
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