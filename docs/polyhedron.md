# `cqmore.polyhedron`

This module provides the `Polyhedron` class and functions for creating `Polyhedron` instances. The `Polyhedron` class defines `points` and `faces` attributes. Here is a way to use them.

    from cqmore.polyhedron import uvSphere
    from cqmore import Workplane

    sphere = (Workplane()
                .polyhedron(*uvSphere(radius = 10, rings = 5))
            )

## Classes

 Signature | Description
--|--
[`Polyhedron(points,faces)`](polyhedron.md#polyhedron) | Define `points` and `faces` attributes.

## Functions

 Signature | Description
--|--
[`uvSphere(radius,[rings])`](polyhedron.md#uvsphere) | Create a UV sphere.

----

# `Polyhedron`

Define a polyhedron.

## Parameters

- `points`: points of vertices. 
- `faces`: face indices.

## Examples     

    from cqmore.polyhedron import Polyhedron
    from cqmore import Workplane

    points = (
        (5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5)
    )

    faces = (
        (0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3)
    )

    tetrahedron = Polyhedron(points, faces)
    tetrahedrons = (Workplane()
                       .rect(15, 15, forConstruction = True)
                       .vertices()
                        .polyhedron(*tetrahedron)
                   )   

![Polyhedron](images/polyhedron_Polyhedron.JPG)

# `uvSphere`

Create a UV sphere.

## Parameters

- `radius`: sphere radius. 
- `rings = 2`: number of horizontal segments.

## Examples 

    from cqmore.polyhedron import uvSphere
    from cqmore import Workplane

    sphere = (Workplane()
                .polyhedron(*uvSphere(radius = 10, rings = 5))
            )

![uvSphere](images/polyhedron_uvSphere.JPG)