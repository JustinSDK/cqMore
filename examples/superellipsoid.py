from cqmore import Workplane
from cqmore.polyhedron import superellipsoid

step = 0.5
cols = 8
rows = 6

superellipsoids = Workplane()
for ei in range(1, cols):
    e = ei * step
    for ni in range(1, rows):
        n = ni * step
        superellipsoids.add(
            Workplane()
                .polyhedron(*superellipsoid(e, n))
                .translate((ei * 2.5, ni * 2.5, 0))
        )
