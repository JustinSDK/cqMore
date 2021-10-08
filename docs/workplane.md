# `cqMore.Workplane`

Define plugins. You may simply use `cqMore.Workplane` to replace `cadquery.Workplane`. For example:

    from cqMore import Workplane

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
             )

You may also attach methods of `cqMore.Workplane` to `cadquery.Workplane`, such as:

    from cadquery import Workplane
    import cqMore

    Workplane.makePolygon = cqMore.Workplane.makePolygon

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
             )

## 2D Operations

 Signature | Description
--|--
[`Workplane.makePolygon(points[,forConstruction])`](workplane.md#makepolygon) | Make a multiple sided wire from `points`.
[`Workplane.intersect2D(toIntersect)`](workplane.md#intersect2d) | Intersect the provided wire from the current wire. 
[`Workplane.union2D(toUnion)`](workplane.md#union2d) | Union the provided wire from the current wire. 
[`Workplane.cut2D(toCut)`](workplane.md#cut2d) | Cut the provided wire from the current wire. 

## 3D Operations

 Signature | Description
--|--
[`Workplane.polyhedron(points,faces[,combine,clean])`](workplane.md#polyhedron) | Create any polyhedron with 3D points(vertices) and faces that enclose the solid.
[`Workplane.surface(points,[thickness,combine,clean])`](workplane.md#surface) | Create a surface with a coordinate meshgrid.

----

# `makePolygon`

Make a multiple sided wire from `points`. 

## Parameters

- `points`: the list of x,y points of the polygon.
- `forConstruction = False`: should the new wires be reference geometry only?

## Examples

    from cqMore import Workplane

    triangle = Workplane().makePolygon(((-2, -2), (2, -2), (0, 2))) 

![makePolygon](images/workplane_makePolygon.JPG)

# `intersect2D`

Intersect the provided wire from the current wire. 

## Parameters

- `toIntersect`: a wire object, or a CQ object having a wire – object to intersect.

## Examples

    from cqMore import Workplane

    r1 = Workplane('YZ').rect(10, 10)
    r2 = Workplane('YZ').center(5, 5).rect(10, 10)
    intersected = r1.intersect2D(r2).extrude(1)

![intersect2D](images/workplane_intersect2D.JPG)

# `union2D`

Union the provided wire from the current wire. 

## Parameters

- `toUnion`: a wire object, or a CQ object having a wire – object to union.       

## Examples 

    from cqMore import Workplane

    r1 = Workplane('YZ').rect(10, 10)
    r2 = Workplane('YZ').center(5, 5).rect(10, 10)
    unioned = r1.union2D(r2).extrude(1)

![union2D](images/workplane_union2D.JPG)

# `cut2D`

Cut the provided wire from the current wire. 

## Parameters

- `toCut`: a wire object, or a CQ object having a wire – object to cut.       

## Examples 

    from cqMore import Workplane

    r1 = Workplane('YZ').rect(10, 10)
    r2 = Workplane('YZ').center(5, 5).rect(10, 10)
    cutted = r1.cut2D(r2).extrude(1)

![cut2D](images/workplane_cut2D.JPG)

# `polyhedron`

Create any polyhedron with 3D points(vertices) and faces that enclose the solid. Each face contains the indices (0 based) of 3 or more points from the `points`.

## Parameters

- `points`: a list of 3D points(vertices).
- `faces`: face indices to fully enclose the solid. When looking at any face from the outside, the face must list all points in a counter-clockwise order.
- `combine = True`: should the results be combined with other solids on the stack (and each other)?
- `clean = True`: call `clean()` afterwards to have a clean shape.

## Examples 

    from cqMore import Workplane

    points = ((5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5))
    faces = ((0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3))
    tetrahedron = Workplane().polyhedron(points, faces)

![polyhedron](images/workplane_polyhedron.JPG)

# `surface`

Create a surface with a coordinate meshgrid.

## Parameters

- `points`: a coordinate meshgrid.
- `thickness = 0`: the amount of being thick (return 2D surface if 0).
- `combine = True`: should the results be combined with other solids on the stack (and each other)?
- `clean = True`: call `clean()` afterwards to have a clean shape.

## Examples 

    from cqMore import *

    def paraboloid(x, y):
        return (x, y, ((y ** 2) - (x ** 2)) / 4)

    min_value = -30
    max_value = 30
    step = 5
    thickness = 0.5

    points = [[
            paraboloid(x / 10, y / 10) 
        for x in range(min_value, max_value, step)
    ] for y in range(min_value, max_value, step)]

    sf = Workplane().surface(points, thickness)

![surface](images/workplane_surface.JPG)