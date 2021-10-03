from .wire import (
    makePolygon,
    intersect2D,
    union2D,
    cut2D
)

from .solid import (
    polyhedron,
    surface
)

from cadquery import (
    Workplane
)

Workplane.makePolygon = makePolygon    
Workplane.intersect2D = intersect2D
Workplane.union2D = union2D
Workplane.cut2D = cut2D

Workplane.polyhedron = polyhedron
Workplane.surface = surface