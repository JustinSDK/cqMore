from cadquery import (
    Vector
)

from typing import (
    cast,
    Iterable
)

from .cq_typing import (
    VectorLike
)

def toVectors(points: Iterable[VectorLike]) -> list[Vector]:
    it = iter(points)
    if isinstance(next(it), Vector):
        return cast(list[Vector], list(points))
    
    return [Vector(*p) for p in points]

def toTuples(points: Iterable[VectorLike]) -> list[tuple]:
    it = iter(points)
    if isinstance(next(it), tuple):
        return cast(list[tuple], list(points))
    
    return [v.toTuple() for v in cast(list[Vector], points)]