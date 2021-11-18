# scikit-image 0.18 or later is required.

import numpy as np
from skimage import measure
from math import sin, cos, radians
from cqmore import Workplane

def gyroid(length, width, height, thickness, step):
    def _gyroid(x, y, z, thickness, length, width, height):
        # is boundary?
        if x == 0 or y == 0 or z == 0 or x == length or y == width or z == height:
            return 0

        half_thickness = thickness / 2

        rx = radians(x)
        ry = radians(y)
        rz = radians(z)
        v = sin(rx) * cos(ry) + sin(ry) * cos(rz) + sin(rz) * cos(rx)
        return 1 if -half_thickness <= v <= half_thickness else 0
    vectorized_gyroid = np.frompyfunc(_gyroid, 7, 1)

    
    l_arange = np.arange(0, length + step, step)
    w_arange = np.arange(0, width + step, step)
    h_arange = np.arange(0, height + step, step)
    x, y, z = np.meshgrid(l_arange, w_arange, h_arange)

    points, faces, _, __ = measure.marching_cubes( # type: ignore
        vectorized_gyroid(x, y, z, thickness, length, width, height), 
        0, 
        spacing = (radians(step),) * 3,
        allow_degenerate = False
    )

    return Workplane().polyhedron(points, faces)


if __name__ == '__main__':
    length = 360
    width = 360
    height = 360
    thickness = 0.4
    step = 10

    g = gyroid(length, width, height, thickness, step)

    # from cadquery import exporters
    # exporters.export(g, 'gyroid.stl')