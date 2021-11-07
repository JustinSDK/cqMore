from cqmore import Workplane
from cqmore.curve import torusKnot, parametricEquation
from cqmore.polygon import star

from cadquery import Plane, Vector

def torus_knot(p, q):
    origin = torusKnot(0, p = p, q = q)
    v1 = Vector(*torusKnot(0.9, p = p, q = q))
    v2 = Vector(*torusKnot(0.1, p = p, q = q))

    return (Workplane(Plane(origin = origin, normal=(v2 - v1)))
               .makePolygon([(p[0] * 0.75, p[1] * 0.75) for p in star()])
               .sweep(
                   Workplane().parametricCurve(
                       parametricEquation(torusKnot, p = p, q = q),
                       N = 96
                   ), 
                   auxSpine = Workplane('XZ').rect(1, 1)
               )
           )

p = 3
q = 2

knot = torus_knot(p, q)