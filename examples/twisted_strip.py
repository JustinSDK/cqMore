
from math import sin, cos, radians
from cqmore import Workplane

u_step = 10
v_step = 0.2
thickness = 0.1

def twisted_strip(u_step, v_step, thickness):
    points = []
    for vi in range(5):
        col = []
        for u in range(0, 720 + u_step, u_step):
            v = -1 + vi * v_step
            col.append((
                (1 + v / 2 * cos(radians(u / 2))) * cos(radians(u)), 
                (1 + v / 2 * cos(radians(u / 2))) * sin(radians(u)), 
                v / 2 * sin(radians(u / 2))
            ))
        
        points.append(col)

    return Workplane().splineApproxSurface(points, thickness)

u_step = 10
v_step = 0.2
thickness = 0.1

strip = twisted_strip(u_step, v_step, thickness)