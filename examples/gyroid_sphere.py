# scikit-image 0.18 or later is required.

from cadquery.cq import T
from gyroid import gyroid
from cqmore import Workplane
from cqmore.polyhedron import uvSphere

def gyroid_sphere(thickness, period):
    length = 370
    width = 370
    height = 370
    step = 10

    g = gyroid(length, width, height, thickness, step)

    offset = 360 - step
    rg = range(period)

    row = Workplane()
    for i in rg:
        row.add(g.translate((offset * i, 0, 0)))

    rect = Workplane()
    for i in rg:
        rect.add(row.translate((0, offset * i, 0)))

    cube = Workplane()
    for i in rg:
        cube.add(rect.translate((0, 0, offset * i)))

    r = 180 * period
    return Workplane().polyhedron(*uvSphere(r, 48, 24)).translate((r, r, r)).intersect(cube)


thickness = 0.4
period = 2
g = gyroid_sphere(thickness, period)

# from cadquery import exporters
# exporters.export(g, 'gyroid_sphere.stl')