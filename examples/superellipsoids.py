from cqmore import Workplane
from cqmore.polyhedron import superellipsoid

step = 0.5
cols = 8
rows = 6

solids = Workplane()
for ei in range(1, cols):
    e = ei * step
    for ni in range(1, rows):
        n = ni * step
        solids.add(
            Workplane()
                .polyhedron(*superellipsoid(e, n, widthSegments = 24, heightSegments = 12))
                .translate((ei * 2.5, ni * 2.5, 0))
        )
