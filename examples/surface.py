from cqMore import *

def paraboloid(x, y):
    return [x, y, ((y ** 2) - (x ** 2)) / 4]

min_value = -30
max_value = 30
step = 5
thickness = 0.5

points = [[
        paraboloid(x / 10, y / 10) 
    for x in range(min_value, max_value, step)
] for y in range(min_value, max_value, step)]


sf = Workplane().surface(points, thickness)
show_object(sf)