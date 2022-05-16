from typing import Iterable, cast, Tuple

from cadquery import Vector
from cadquery.cq import VectorLike

# Signum function
def signum(n):
    return n and (1, -1)[n < 0]

def toVectors(points: Iterable[VectorLike]) -> Tuple[Vector]:
    if isinstance(next(iter(points)), Vector):
        return cast(tuple[Vector], list(points))
    
    return cast(Tuple[Vector], tuple(Vector(*p) for p in points))


def toTuples(points: Iterable[VectorLike]) -> Tuple[Tuple]:
    if isinstance(next(iter(points)), Tuple):
        return cast(tuple[tuple], tuple(points))

    r = tuple(v.toTuple() for v in cast(tuple[Vector], points))
    return cast(tuple[tuple], r)
