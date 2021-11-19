# scikit-image 0.18 or later is required.

from math import radians
from gyroid import gyroid
from cqmore import Workplane
from cqmore.polyhedron import uvSphere

def gyroid_sphere(thickness, period, step):
    width = 360 + step * 5

    g = gyroid(width, width, width, thickness, step)
    
    r = radians(180 * period)

    if period == 1:
        return Workplane().polyhedron(*uvSphere(r, 48, 24)).translate((r, r, r)).intersect(g)

    offset = radians(360)
    rg = range(period)

    row = Workplane()
    for i in rg:
        row.add(g.translate((offset * i, 0, 0)))
    row = row.combine()

    rect = Workplane()
    for i in rg:
        rect.add(row.translate((0, offset * i, 0)))
    rect = rect.combine()

    cube = Workplane()
    for i in rg:
        cube.add(rect.translate((0, 0, offset * i)))
    cube = cube.combine()

    return Workplane().polyhedron(*uvSphere(r, 48, 24)).translate((r, r, r)).intersect(cube)


thickness = 0.4
period = 2
step = 10
g = gyroid_sphere(thickness, period, step)

# from cadquery import exporters
# exporters.export(g, 'gyroid_sphere.stl')