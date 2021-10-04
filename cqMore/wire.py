from cadquery import (
    Vector,
    Wire, 
    Workplane,
    DirectionSelector
)

from typing import (
    Iterable
)

from .cq_typing import (
    T,
    VectorLike
)

def bool2D(workplane: T, toBool: T, boolMethod: str) -> T:
    toExtruded = (
        Workplane(toBool.plane)
            .add(toBool.vals())
            .toPending()
    )
    booled = Workplane.__dict__[boolMethod](workplane.extrude(1), toExtruded.extrude(1))
    planeZdir = DirectionSelector(-workplane.plane.zDir)
    return booled.faces(planeZdir).wires().toPending()

def makePolygon(points: Iterable[VectorLike], forConstruction: bool = False) -> Wire:
    vts = [Vector(*p) for p in points]
    vts.append(vts[0])
    return Wire.makePolygon(vts, forConstruction)