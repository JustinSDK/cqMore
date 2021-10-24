from cqmore import Workplane
from cqmore.curve import torusKnot

p = 11
q = 13

c = (Workplane()
         .polyline([torusKnot(t / 360, p, q) for t in range(360)])
         .close()
    )