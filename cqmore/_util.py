from typing import Iterable, cast

from cadquery import Vector
from cadquery.cq import VectorLike

# Signum function
def signum(n):
    return n and (1, -1)[n < 0]

def toVectors(points: Iterable[VectorLike]) -> tuple[Vector]:
    if isinstance(next(iter(points)), Vector):
        return cast(tuple[Vector], list(points))
    
    return cast(tuple[Vector], tuple(Vector(*p) for p in points))


def toTuples(points: Iterable[VectorLike]) -> tuple[tuple]:
    if isinstance(next(iter(points)), tuple):
        return cast(tuple[tuple], tuple(points))

    r = tuple(v.toTuple() for v in cast(tuple[Vector], points))
    return cast(tuple[tuple], r)
