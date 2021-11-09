from typing import Iterable, cast

from cadquery import Vector
from cadquery.cq import VectorLike


def toVectors(points: Iterable[VectorLike]) -> tuple[Vector]:
    it = iter(points)
    if isinstance(next(it), Vector):
        return cast(tuple[Vector], list(points))
    
    return cast(tuple[Vector], tuple(Vector(*p) for p in points))


def toTuples(points: Iterable[VectorLike]) -> tuple[tuple]:
    it = iter(points)
    if isinstance(next(it), tuple):
        return cast(tuple[tuple], tuple(points))

    r = tuple(v.toTuple() for v in cast(tuple[Vector], points))
    return cast(tuple[tuple], r)
