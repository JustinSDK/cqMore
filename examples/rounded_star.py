from cqmore import Workplane
from cqmore.polygon import star
from cadquery import Edge, Vector, Wire

def roundedStar(outerRadius: float = 1, innerRadius: float = 0.381966, n: int = 5, rounded: float = 0.5, spoke: float = 0.381966) -> Wire:
    pts = list(star(outerRadius, innerRadius, n))
    ts = rounded / outerRadius * 3 # tangent scale
    spokes = [1, spoke]
    tangents = [
        Vector(-ts * pts[i][1] / spokes[i % 2], ts * pts[i][0] / spokes[i % 2], 0)
        for i in range(len(pts))
    ]

    return Wire.assembleEdges([Edge.makeSpline(listOfVector = [Vector(*p) for p in pts], tangents = tangents, periodic = True, scale = False)])

outerRadius = 1
innerRadius = 0.381966
n = 5
rounded = 0.5
spoke = 0.381966

w = (Workplane()
        .add(roundedStar(outerRadius, innerRadius, n, rounded, spoke))
        .toPending()
        .extrude(1)
    )