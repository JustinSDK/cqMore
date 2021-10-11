from cqmore import Workplane

points = (
    (5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5)
)

faces = (
    (0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3)
)

tetrahedron = Workplane().polyhedron(points, faces)
# show_object(tetrahedron)