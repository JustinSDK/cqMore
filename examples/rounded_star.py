from cqmore import Workplane
from cqmore.polygon import star
from cadquery import Edge, Vector, Wire

def roundedStar(outerRadius: float = 1, innerRadius: float = 0.381966, n: int = 5, rounded: float = 0.5, spoke: float = 0.381966) -> Wire:
    vts = [Vector(*p) for p in star(outerRadius, innerRadius, n)]
    ts = rounded / outerRadius * 3 # tangent scale
    spokes = [1, spoke]
    tangents = [
        Vector(-ts * vts[i].y / spokes[i % 2], ts * vts[i].x / spokes[i % 2], 0)
        for i in range(len(vts))
    ]

    return Wire.assembleEdges(
        [Edge.makeSpline(listOfVector = vts, tangents = tangents, periodic = True, scale = False)]
    )

outerRadius = 1
innerRadius = 0.381966
n = 5
rounded = 0.5
spoke = 0.381966

w = (Workplane()
        .add(roundedStar(outerRadius, innerRadius, n, rounded, spoke))
    )