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