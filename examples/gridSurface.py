from math import sqrt, cos, radians
from cqmore import Workplane

def ripple(x: float, y: float):
    n = radians(sqrt(x ** 2 + y ** 2))
    return (x, y, 30 * (cos(n) + cos(3 * n)))

min_value = -200
max_value = 200
step = 10
thickness = 5

points = [[
        ripple(x, y) 
    for x in range(min_value, max_value, step)
] for y in range(min_value, max_value, step)]

sf = Workplane().gridSurface(points, thickness)
# show_object(sf)