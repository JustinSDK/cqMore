from cqmore import Workplane
from cqmore.matrix import Matrix3D
from cqmore.polyhedron import sweep

profile = [(10, -1, 0), (10, 1, 0), (-10, 1, 0), (-10, -1, 0)]

mat = Matrix3D()
translation = mat.translate((20, 0, 0))
rotationX = mat.rotateX(90)

step = 15
sects = []
for i in range(24):
    m = mat.rotateZ(i * step) * translation * rotationX * mat.rotateZ(i * step / 2)
    s = [m.transform(p) for p in profile]
    sects.append(s)

rotationX = Workplane().polyhedron(
                *sweep(sects, close_idx = 2)
            )