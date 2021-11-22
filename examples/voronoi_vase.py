# Scipy 1.6 or later is required.
# not stable, float-error problems? 
# Keep on trying until you make it ... XD

from random import random
import numpy
from scipy import spatial
from cadquery import Vector
from cqmore import Workplane
from cqmore.matrix import translation, scaling
from cqmore.polygon import regularPolygon
from cqmore.polyhedron import sweep

diameter = 90
sides = 12
height = 120
thickness = 2
step = 30

def voronoi_vase(diameter, sides, height, thickness, step):
    def sided_vase(diameter, sides, height):
        r = diameter / 2

        half_height = height / 2
        radii = [r * 0.5, r * 0.8, r, r * 0.875, r * 0.725, r * 0.625, r * 0.6, r * 0.75]
        h_step = height / len(radii)
        sections = []
        for i in range(len(radii)):
            polygon = regularPolygon(sides,  radii[i])
            sections.append([(p[0], p[1], -half_height + h_step * i) for p in polygon])
        
        return Workplane().polyhedron(*sweep(sections))

    def random_points(diameter, height, step):
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
        return points
   
    def voronoiConvexs(diameter, height, thickness, step):
        voronoi = spatial.Voronoi(random_points(diameter, height, step))
        vertices = numpy.around(voronoi.vertices, 5)

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

        return convexs

    vase = sided_vase(diameter, sides, height)

    outerShell = vase.faces('+Z').shell(thickness)
    innerShell = vase.faces('+Z').shell(-thickness)
    
    return (outerShell
               .intersect(voronoiConvexs(diameter, height, thickness, step))
               .union(innerShell)
           )
    
vase = voronoi_vase(diameter, sides, height, thickness, step)
