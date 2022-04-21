from typing import Iterable, Union, cast

from cadquery import DirectionSelector, Wire, Workplane, Vector
from cadquery.cq import T, VectorLike

from ._util import toTuples, toVectors

from .polygon import hull2D


def bool2D(workplane: T, toBool: Union[T, Wire], boolMethod: str) -> T:
    if isinstance(toBool, Workplane):
        toExtruded = (
            Workplane(workplane.plane)
                .add(toBool.ctx.pendingWires)
                .toPending()
        )
    elif isinstance(toBool, Wire):
        toExtruded = (
            Workplane(workplane.plane)
                .add(toBool)
                .toPending()
        )
    else:
        raise ValueError(f"Cannot {boolMethod} type '{type(toBool)}'")
    
    booled = Workplane.__dict__[boolMethod](workplane.extrude(1), toExtruded.extrude(1))
    planeZdir = DirectionSelector(-workplane.plane.zDir)
    return booled.faces(planeZdir).wires().toPending()

def makePolygon(points: Iterable[VectorLike], forConstruction: bool = False) -> Wire:
    vts = toVectors(points)
    return Wire.makePolygon(vts + (vts[0], ), forConstruction)


def polylineJoinWire(points: Iterable[VectorLike], join: Union[T, Wire], forConstruction: bool = False) -> Wire:
    if isinstance(join, Workplane):
        join_wire = cast(Wire, join.val())
    elif isinstance(join, Wire):
        join_wire = join
    else:
        raise ValueError(f"Join type '{type(join)}' is not allowed")
    
    join_vts = tuple(v.toTuple() for v in join_wire.Vertices())
    joins = tuple(
        tuple(
            Vector(p) + Vector(vt) for (*vt, _) in join_vts
        )
        for p in toTuples(points)
    )

    wp = Workplane()
    for i in range(len(joins) - 1):
        wp = wp.add(
            Workplane(makePolygon(hull2D(joins[i] + joins[i + 1]), forConstruction))
                .toPending()
                .extrude(1)
        )

    wire = cast(Wire, wp.combine().faces('<Z').wires().val())
    wire.forConstruction = forConstruction
    return wire
