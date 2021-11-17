# scikit-image 0.18 or later is required.

import numpy as np
from skimage import measure
from math import sin, cos, radians
from cqmore import Workplane

def gyroid(length, width, height, thickness):
    def _gyroid(x, y, z, thickness, l_end, w_end, h_end):
        # is boundary?
        if x == 0 or y == 0 or z == 0 or x == l_end or y == w_end or z == h_end:
            return 0

        half_thickness = thickness / 2

        rx = radians(x)
        ry = radians(y)
        rz = radians(z)
        v = sin(rx) * cos(ry) + sin(ry) * cos(rz) + sin(rz) * cos(rx)
        return 1 if -half_thickness <= v <= half_thickness else 0
    vectorized_gyroid = np.frompyfunc(_gyroid, 7, 1)

    step = thickness * 25
    l_end = length - step
    w_end = width - step
    h_end = height - step
    l_arange = np.arange(0, length, step)
    w_arange = np.arange(0, width, step)
    h_arange = np.arange(0, height, step)
    x, y, z = np.meshgrid(l_arange, w_arange, h_arange)

    points, faces, _, __ = measure.marching_cubes( # type: ignore
        vectorized_gyroid(x, y, z, thickness, l_end, w_end, h_end), 
        0, 
        spacing = (step, step, step),
        allow_degenerate = False
    )

    return Workplane().polyhedron(points, faces)

if __name__ == '__main__':
    length = 360
    width = 360
    height = 360
    thickness = 0.4

    g = gyroid(length, width, height, thickness)

    # from cadquery import exporters
    # exporters.export(g, 'gyroid.stl')