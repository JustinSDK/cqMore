from cqmore import Workplane
from cqmore.matrix import translation, rotationX, rotationZ
from cqmore.polyhedron import sweep

profile = [(10, -1, 0), (10, 1, 0), (-10, 1, 0), (-10, -1, 0)]

translationX20 = translation((20, 0, 0))
rotationX90 = rotationX(90)

frags = 24
angle_step = 360 / frags
profiles = []
for i in range(frags):
    m = rotationZ(i * angle_step) @ translationX20 @ rotationX90 @ rotationZ(i * angle_step / 2)
    profiles.append([m.transform(p) for p in profile])

r = Workplane().polyhedron(*sweep(profiles, close_idx = 2))