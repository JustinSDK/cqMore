from cqmore import Workplane

r1 = Workplane('YZ').rect(10, 10)
r2 = Workplane('YZ').center(5, 5).rect(10, 10)
r3 = Workplane('YZ').center(-2, -2).rect(10, 10)
r4 = r1.intersect2D(r2).intersect2D(r3)

# show_object([r1, r2, r3])
# show_object(r4.extrude(1))
