from cadquery import (
    Wire, 
    Workplane,
    DirectionSelector
)

from typing import (
    Iterable,
    Union,
    cast
)

from .cq_typing import (
    T,
    Point2D,
    VectorLike
)

from .util import (
    toVectors, 
    toTuples
)

def bool2D(workplane: T, toBool: Union[T, Wire], boolMethod: str) -> T:
    if isinstance(toBool, Workplane):
        toExtruded = (
            Workplane(toBool.plane)
                .add(toBool.vals())
                .toPending()
        )
    elif isinstance(toBool, Wire):
        toExtruded = (
            Workplane()
                .add(toBool)
                .toPending()
        )
    else:
        raise ValueError("Cannot {} type '{}'".format(boolMethod, type(toBool)))
    
    booled = Workplane.__dict__[boolMethod](workplane.extrude(1), toExtruded.extrude(1))
    planeZdir = DirectionSelector(-workplane.plane.zDir)
    return booled.faces(planeZdir).wires().toPending()

def makePolygon(points: Iterable[VectorLike], forConstruction: bool = False) -> Wire:
    vts = toVectors(points)
    vts.append(vts[0])
    return Wire.makePolygon(vts, forConstruction)

def hull2D(points: Iterable[VectorLike]) -> list[Point2D]:
    def _cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    pts = sorted(toTuples(points))
    leng = len(pts)
    convex_hull = [pts[0], pts[1]]

    # lower bound
    for i in range(2, leng):
        while len(convex_hull) >= 2 and _cross(convex_hull[-2], convex_hull[-1], pts[i]) <= 0:
            convex_hull.pop()
        convex_hull.append(pts[i])
    
    # upper bound
    upper_bound_start = len(convex_hull) + 1
    for i in range(leng - 2, -1, -1):
        while len(convex_hull) >= upper_bound_start and _cross(convex_hull[-2], convex_hull[-1], pts[i]) <= 0:
            convex_hull.pop()
        convex_hull.append(pts[i])
    
    return cast(list[Point2D], convex_hull)

def polylineJoinWire(points: Iterable[VectorLike], join: Union[T, Wire], forConstruction: bool = False) -> Wire:
    if isinstance(join, Workplane):
        join_wire = cast(Wire, join.val())
    elif isinstance(join, Wire):
        join_wire = join
    else:
        raise ValueError("Join type '{}' is not allowed".format(type(join)))
    
    pts = toTuples(points)
    join_vts = [v.toTuple() for v in join_wire.Vertices()]
    joins = [[(p[0] + vt[0], p[1] + vt[1]) for vt in join_vts] for p in pts]
    workplanes = [
        Workplane(makePolygon(hull2D(joins[i] + joins[i + 1]), forConstruction)).toPending()
        for i in range(len(pts) - 1)
    ]

    wp = workplanes[0].extrude(1)
    for i in range(1, len(workplanes)):
        wp = wp.union(workplanes[i].extrude(1))

    wire = cast(Wire, wp.faces('<Z').wires().val())
    wire.forConstruction = forConstruction
    return wire
