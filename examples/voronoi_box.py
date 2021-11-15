# Scipy 1.6 or later is required.

import numpy
from scipy import spatial
from cadquery import Vector
from cqmore import Workplane
from cqmore.matrix import translation, scaling

def voronoi_box(n, length, width, height, thickness):
    points = numpy.random.rand(n, 3) * max(length, width, height) * 2
    voronoi = spatial.Voronoi(points)
    # round for avoiding floating-point error
    vertices = numpy.around(voronoi.vertices, decimals = 5)

    m_scaling = scaling((0.9, 0.9, 0.9))

    convexs = Workplane()
    convex = Workplane()
    for region_i in voronoi.point_region:
        region = voronoi.regions[region_i]
        region_vts = [Vector(*vertices[i]) for i in region if i != -1]
        geom_center = sum(region_vts, Vector()) / len(region_vts)
        m = translation(geom_center.toTuple()) @ m_scaling @ translation((-geom_center).toTuple())
        transformed = m.transformAll(v.toTuple() for v in region_vts)
        convexs.add(convex.hull(transformed))

    half_thickness = thickness / 2
    voronoi_frame = (
        Workplane()
            .box(length - half_thickness, width - half_thickness, height - half_thickness)
            .faces('+Z')
            .shell(thickness)
            .translate((length, width, height))
            .cut(convexs)
            .translate((-length, -width, -height + thickness / 8))
    )

    box = (Workplane()
              .box(length, width, height - thickness / 4)
              .faces('+Z')
              .shell(half_thickness)
          )
    
    return voronoi_frame.union(box)

n = 30
length = 60
width = 60
height = 60
thickness = 3

box = voronoi_box(n, length, width, height, thickness)