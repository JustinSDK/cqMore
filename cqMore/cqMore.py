from .wire import (
    makePolygon,
    bool2D
)

from .solid import (
    polyhedron,
    surface
)

from typing import (
    Iterable
)

from .cq_typing import (
    T,
    VectorLike
)

import cadquery

class Workplane(cadquery.Workplane):
    def makePolygon(self: T, points: Iterable[VectorLike], forConstruction: bool = False) -> T:
        p = makePolygon(points, forConstruction)
        return self.eachpoint(lambda loc: p.moved(loc), True)

    def intersect2D(self: T, toIntersect: T) -> T:
        return bool2D(self, toIntersect, 'intersect')
        
    def union2D(self: T, toUnion: T) -> T:
        return bool2D(self, toUnion, 'union')

    def cut2D(self: T, toCut: T) -> T:
        return bool2D(self, toCut, 'cut')

Workplane.polyhedron = polyhedron
Workplane.surface = surface