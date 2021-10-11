from cqmore import Workplane

points = (
    (50, 50, 50),
    (50, 50, 0),
    (-50, 50, 0),
    (-50, -50, 0),
    (50, -50, 0),
    (0, 0, 50),
    (0, 0, -50)
)

convex_hull = Workplane().hull(points)
