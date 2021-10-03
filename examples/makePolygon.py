from cqMore import *
from math import cos, sin, radians     

fn = 12
r = 5
a_step = radians(360 / fn)

points = [
    (r * cos(a_step * i), r * sin(a_step * i)) 
         for i in range(fn)
]

polygon = (Workplane()
              .rect(30, 30, forConstruction = True)
              .vertices()
              .makePolygon(points)
          )
       
show_object(polygon)