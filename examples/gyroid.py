# scikit-image 0.18 or later is required.

import numpy as np
from skimage import measure
from math import sin, cos, radians
from cqmore import Workplane

def gyroid(x, y, z, thickness, end):
    # is boundary?
    if x == 0 or y == 0 or z == 0 or x == end or y == end or z == end:
        return 0

    half_thickness = thickness / 2

    rx = radians(x)
    ry = radians(y)
    rz = radians(z)
    v = sin(rx) * cos(ry) + sin(ry) * cos(rz) + sin(rz) * cos(rx)
    return 1 if -half_thickness < v < half_thickness else 0
vectorized_gyroid = np.frompyfunc(gyroid, 5, 1)


width = 360
step = 10
thickness = 0.4

end = width - step
arange = np.arange(0, width, step)
x, y, z = np.meshgrid(arange, arange, arange)

points, faces, _, __ = measure.marching_cubes( # type: ignore
    vectorized_gyroid(x, y, z, thickness, end), 
    0, 
    allow_degenerate = False
)

g = Workplane().polyhedron(points, faces)

# from cadquery import exporters
# exporters.export(g, 'gyroid.stl')