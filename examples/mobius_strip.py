from math import sin, cos, radians
from cqmore import Workplane
from cqmore.polyhedron import gridSurface

u_step = 10
v_step = 0.2
thickness = 0.1

# not precise, but workable
points = []
for vi in range(11):
    row = []
    for u in range(0, 360 + u_step, u_step):
        v = -1 + vi * v_step
        row.append((
            (1 + v / 2 * cos(radians(u / 2))) * cos(radians(u)), 
            (1 + v / 2 * cos(radians(u / 2))) * sin(radians(u)), 
            v / 2 * sin(radians(u / 2))
        ))
    
    points.append(row)

mobius_strip = Workplane().polyhedron(*gridSurface(points, thickness))