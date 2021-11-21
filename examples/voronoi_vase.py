# Scipy 1.6 or later is required.
# not stable, float-error problems? 
# Keep on trying until you make it ... XD


from random import random
from scipy import spatial
from cadquery import Vector
from cqmore import Workplane
from cqmore.matrix import translation, scaling
import numpy

diameter = 90
height = 120
thickness = 2
step = 30

def voronoi_vase(diameter, height, thickness, step):
    random_scale = step / 2
    double_step = step * 2
    half_random_scale = random_scale / 2
    x_offset = -diameter / 2 - half_random_scale
    y_offset = -diameter / 2 - half_random_scale
    z_offset = -height / 2 - half_random_scale

    points = []
    for x in range(-double_step, diameter + double_step, step):
        for y in range(-double_step, diameter + double_step, step):
            for z in range(-double_step, height + double_step, step):
                points.append([
                    x_offset + x + random() * random_scale, 
                    y_offset + y + random() * random_scale, 
                    z_offset + z + random() * random_scale]
                )

    voronoi = spatial.Voronoi(points)
    vertices = numpy.around(voronoi.vertices, 6)

    s = (step - thickness) / step
    m_scaling = scaling((s, s, s))

    convex = Workplane()
    convexs = Workplane()
    for region_i in voronoi.point_region:
        region = voronoi.regions[region_i]
        region_vts = [Vector(*vertices[i]) for i in region if i != -1]
        geom_center = sum(region_vts, Vector()) / len(region_vts)
        m = translation(geom_center.toTuple()) @ m_scaling @ translation((-geom_center).toTuple())
        transformed = m.transformAll(v.toTuple() for v in region_vts)
        convexs.add(convex.hull(transformed))

    r = diameter / 2
    vasePath = [
        (0, 0),
        (height, 0),
        (height, r * 0.5),
        (height * 0.85, r * 0.8),
        (height * 0.675, r),
        (height * 0.5, r * 0.875),
        (height * 0.34, r * 0.725),
        (height * 0.215, r * 0.625),
        (height * 0.1, r * 0.6),
        (0, r * 0.75)
    ]

    return (Workplane()
               .polyline(vasePath).close()
               .revolve(360, (0, 0, 0), (1, 0, 0))
               .rotate((0, 0, 0), (0, 1, 0), 90)
               .translate((0, 0, height / 2))
               .cut(convexs)
           )
    
vase = voronoi_vase(diameter, height, thickness, step)
