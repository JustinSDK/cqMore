from cqmore import Workplane
from cqmore.polyhedron import (
    tetrahedron, 
    hexahedron, 
    octahedron, 
    dodecahedron, 
    icosahedron
)

radius = 15
thickness = 1.25

polyhedra = [
    tetrahedron, 
    hexahedron, 
    octahedron, 
    dodecahedron, 
    icosahedron
]

for i in range(5):
    polyhedron = (Workplane()
                    .polyhedron(*(polyhedra[i](radius)))
                    .faces()
                 )

    r = polyhedron.item(0).shell(-thickness)
    for j in range(1, polyhedron.size()):
        r = r.intersect(polyhedron.item(j).shell(-thickness))

    show_object(r.translate((radius * i * 2, 0, 0))) # type: ignore