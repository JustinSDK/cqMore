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
    VectorLike,
    FaceIndices,
    MeshGrid
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

    def polyhedron(self: T, points: Iterable[VectorLike], faces: Iterable[FaceIndices], combine: bool = True, clean: bool = True) -> T:
        poly = polyhedron(points, faces)
        poly_all = self.eachpoint(lambda loc: poly.moved(loc), True)
        
        if not combine:
            return poly_all
        else:
            return self.union(poly_all, clean=clean)

    def surface(self: T, points: MeshGrid, thickness: float, combine: bool = True, clean: bool = True) -> T:
        sf = surface(points, thickness)
        sf_all = self.eachpoint(lambda loc: sf.moved(loc), True)
        
        if not combine:
            return sf_all
        else:
            return self.union(sf_all, clean=clean)