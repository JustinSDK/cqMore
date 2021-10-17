from cqmore import Workplane
from cqmore.polyhedron import tetrahedron, hexahedron, octahedron, dodecahedron, icosahedron

number_of_faces = 12 # 4, 6, 8, 12 or 20
radius = 10
font_name = 'Arial Black'
font_size = 5
font_distance = 1

platonic_polyhedra = {
    4: tetrahedron, 
    6: hexahedron, 
    8: octahedron, 
    12: dodecahedron, 
    20: icosahedron
}

dice = (Workplane()
           .polyhedron(
               *platonic_polyhedra[number_of_faces](radius)
           )
       )

faces = dice.faces().vals()
for i in range(len(faces)):
    dice = dice.cut(
        Workplane(faces[i])
            .workplane()
            .text(
                str(number_of_faces - i), 
                font_size, 
                -font_distance,
                font = font_name
            )
    )