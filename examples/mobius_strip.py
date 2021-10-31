from cqmore import Workplane
from cqmore.matrix import translation, rotationX, rotationZ
from cqmore.polyhedron import sweep

profile = [(10, -1, 0), (10, 1, 0), (-10, 1, 0), (-10, -1, 0)]

translationX20 = translation((20, 0, 0))
rotationX90 = rotationX(90)

angle_step = 15
profiles = []
for i in range(24):
    m = rotationZ(i * angle_step) * translationX20 * rotationX90 * rotationZ(i * angle_step / 2)
    profiles.append([m.transform(p) for p in profile])

rotationX = Workplane().polyhedron(
                *sweep(profiles, close_idx = 2)
            )