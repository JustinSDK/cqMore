from cqmore import Workplane
from cqmore.matrix import translation, rotationX, rotationZ
from cqmore.polyhedron import sweep

def mobius_strip(radius, frags):
    profile = [(10, -1, 0), (10, 1, 0), (-10, 1, 0), (-10, -1, 0)]

    translationX20 = translation((radius, 0, 0))
    rotationX90 = rotationX(90)

    angle_step = 360 / frags
    profiles = []
    for i in range(frags):
        m = rotationZ(i * angle_step) @ translationX20 @ rotationX90 @ rotationZ(i * angle_step / 2)
        profiles.append(m.transformAll(profile))

    return Workplane().polyhedron(*sweep(profiles, closeIdx = 2))

radius = 20
frags = 24

strip = mobius_strip(radius, frags)