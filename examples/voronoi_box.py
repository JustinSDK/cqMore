# Scipy 1.6 or later is required.

import numpy
from scipy import spatial
from cadquery import Vector
from cqmore import Workplane
from cqmore.matrix import translation, scaling

n = 50
width = 60
thickness = 3

points = numpy.random.rand(n, 3) * width * 2
voronoi = spatial.Voronoi(points)
m_scaling = scaling((0.9, 0.9, 0.9))
convexs = Workplane()
convex = Workplane()
for region_i in voronoi.point_region:
    region = voronoi.regions[region_i]
    region_vts = [Vector(*voronoi.vertices[i]) for i in region if i != -1]
    geom_center = sum(region_vts, Vector()) / len(region_vts)
    m = translation(geom_center.toTuple()) @ m_scaling @ translation((-geom_center).toTuple())
    transformed = m.transformAll([v.toTuple() for v in region_vts])
    convexs.add(
        convex.hull(
            # round for avoiding floating-point error
            tuple((round(p[0], 2), round(p[1], 2), round(p[2], 2)) for p in transformed)
        )
    )

half_thickness = thickness / 2
voronoi_frame = (
    Workplane()
        .box(width - half_thickness, width - half_thickness, width - half_thickness)
        .faces('+Z')
        .shell(thickness)
        .translate((width, width, width))
        .cut(convexs)
)

inner_width = width
box = (Workplane()
          .box(inner_width, inner_width, inner_width - thickness / 4)
          .faces('+Z')
          .shell(half_thickness)
          .translate((width, width, width - thickness / 8))
      )

show_object( # type: ignore
    voronoi_frame.union(box)
                 .translate((-width, -width, -width))
) 