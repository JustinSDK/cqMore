# Scipy 1.6 or later is required.

from random import random
import numpy
from scipy import spatial
from cadquery import Vector
from cqmore import Workplane
from cqmore.matrix import translation, scaling

length = 60
width = 60
height = 120
thickness = 2
step = 30
cube_frame = True

def voronoi_cube(length, width, height, thickness, step):
    def random_points(length, width, height, step):
        random_scale = step / 2
        double_step = step * 2
        half_random_scale = random_scale / 2
        x_offset = -length / 2 - half_random_scale
        y_offset = -width / 2 - half_random_scale
        z_offset = -height / 2 - half_random_scale

        points = []
        for x in range(-double_step, length + double_step, step):
            for y in range(-double_step, width + double_step, step):
                for z in range(-double_step, height + double_step, step):
                    points.append([
                        x_offset + x + random() * random_scale, 
                        y_offset + y + random() * random_scale, 
                        z_offset + z + random() * random_scale]
                    )
        return points

    def voronoiConvexs(length, width, height, thickness, step):
        voronoi = spatial.Voronoi(random_points(length, width, height, step))
        vertices = numpy.around(voronoi.vertices, decimals = 5)

        s = (step - thickness) / step
        m_scaling = scaling((s, s, s))

        convexs = Workplane()
        convex = Workplane()
        for region_i in voronoi.point_region:
            region = voronoi.regions[region_i]
            region_vts = [Vector(*vertices[i]) for i in region if i != -1]
            geom_center = sum(region_vts, Vector()) / len(region_vts)
            m = translation(geom_center.toTuple()) @ m_scaling @ translation((-geom_center).toTuple())
            transformed = m.transformAll(v.toTuple() for v in region_vts)
            convexs.add(convex.hull(transformed))
        return convexs

    
    return (Workplane()
               .box(length, width, height)
               .cut(voronoiConvexs(length, width, height, thickness, step)
           )
)


def makeFrame(polyhedron):
    faces = polyhedron.faces()
    frame = faces.item(0).shell(-thickness)
    for j in range(1, faces.size()):
        frame = frame.intersect(faces.item(j).shell(-thickness))
    return frame

cube = voronoi_cube(length, width, height, thickness, step)

if cube_frame:
    cube = makeFrame(Workplane().box(length, width, height)).union(cube)

show_object(cube) # type: ignore