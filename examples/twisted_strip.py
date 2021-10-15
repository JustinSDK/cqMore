from math import sin, cos, radians
from cqmore import Workplane

u_step = 10
v_step = 0.2
thickness = 0.1

points = []
for u in range(0, 720 + u_step, u_step):
    row = []
    for vi in range(5):
        v = -1 + vi * v_step
        row.append((
            (1 + v / 2 * cos(radians(u / 2))) * cos(radians(u)), 
            (1 + v / 2 * cos(radians(u / 2))) * sin(radians(u)), 
            v / 2 * sin(radians(u / 2))
        ))
    
    points.append(row)

twisted_strip = Workplane().gridSurface(points, thickness)