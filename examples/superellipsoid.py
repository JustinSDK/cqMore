from cqmore import Workplane
from cqmore.polyhedron import superellipsoid

r = Workplane().polyhedron(*superellipsoid(0.5, 2.8))