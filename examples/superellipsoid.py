from math import pi, tau, sin, cos
from cqmore import Workplane

def superellipsoid(e, n, frags):
    def _sgn(x):
        if x < 0:
            return -1
        elif x == 0:
            return 0
        else:
            return 1
    
    def _c(w, m):
        cosw = cos(w)
        return _sgn(cosw) * pow(abs(cosw), m)

    def _s(w, m):
        sinw = sin(w)
        return _sgn(sinw) * pow(abs(sinw), m)

    a = 1
    b = 1
    c = 1

    step = tau / frags
    sections = []
    for vi in range(2, frags // 2 - 1):
        v = -pi / 2 + vi * step
        section = []
        for ui in range(frags):
            u = ui * step
            x = a * _c(v, n) * _c(u, e)
            y = b * _c(v, n) * _s(u, e)
            z = c * _s(v, n)
            section.append((x, y, z))
        sections.append(section)
    
    return sections


sections = superellipsoid(0.5, 2.8, 96)

r = Workplane()
path = []
for i in range(len(sections)):
    r.add(Workplane().makePolygon(sections[i], forConstruction=True)).toPending()
    path.append((0, 0, sections[i][0][2]))

r = r.sweep(Workplane().polyline(path), multisection = True)