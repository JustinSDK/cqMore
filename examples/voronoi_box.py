import numpy
from scipy import spatial
from cadquery import Vector
from cqmore import Workplane
from cqmore.polyhedron import Polyhedron
from cqmore.matrix import translation, scaling

def hull3D(points):
    hull = spatial.ConvexHull(points)
    vertices = [points[i] for i in hull.vertices]
    v_i_lookup = {v: i for i, v in enumerate(vertices)}
    faces = [
        tuple(v_i_lookup[points[i]] for i in face)
        for face in hull.simplices
    ]

    return Polyhedron(vertices, faces)

n = 50
width = 50
thickness = 2

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
    convexs.add(
        convex.polyhedron(
            *hull3D(m.transformAll([v.toTuple() for v in region_vts]))
        )
    )

half_thickness = thickness / 2
offset = (width, width, width)
voronoi_frame = (Workplane()
        .box(width, width, width)
        .faces('+Z')
        .shell(thickness * 0.75)
        .translate(offset)
        .cut(convexs)
    )

inner_width = width + half_thickness
box = Workplane().box(inner_width, inner_width, inner_width).faces('+Z').shell(-half_thickness).translate(offset)
show_object(voronoi_frame.union(box).translate((-width, -width, -width))) # type: ignore