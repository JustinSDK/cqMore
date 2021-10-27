# `cqmore.Workplane`

Define plugins. You may simply use `cqmore.Workplane` to replace `cadquery.Workplane`. For example:

    from cqmore import Workplane

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
             )

You may also attach methods of `cqmore.Workplane` to `cadquery.Workplane`, such as:

    from cadquery import Workplane
    import cqmore
    cqmore.extend(Workplane)

    result = (Workplane()
                .rect(10, 10)
                .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2)))
                .extrude(1)
            )

## 2D Operations

 Signature | Description
--|--
[`makePolygon(points[,forConstruction])`](workplane.md#makepolygon) | Make a multiple sided wire through the provided points.
[`intersect2D(toIntersect)`](workplane.md#intersect2d) | Intersect the provided wire from the current wire. 
[`union2D(toUnion)`](workplane.md#union2d) | Union the provided wire from the current wire. 
[`cut2D(toCut)`](workplane.md#cut2d) | Cut the provided wire from the current wire. 
[`hull2D([points,forConstruction])`](workplane.md#hull2d) | Create a convex hull through the provided points. 
[`polylineJoin2D(points,join[,forConstruction])`](workplane.md#polylineJoin2D) | Place a join on each point. Hull each pair of joins and union all convex hulls.

## 3D Operations

 Signature | Description
--|--
[`splineApproxSurface(points[,thickness,combine,clean])`](workplane.md#splineApproxSurface) | Approximate a spline surface through the provided points.
[`polyhedron(points,faces[,combine,clean])`](workplane.md#polyhedron) | Create any polyhedron through 3D points(vertices) and faces that enclose the solid.
[`hull([points,combine,clean])`](workplane.md#hull) | Create a convex hull through the provided points. 
[`polylineJoin(points,join[,combine,clean])`](workplane.md#polylineJoin) | Place a join on each point. Hull each pair of joins and union all convex hulls.

----

# `makePolygon`

Make a multiple sided wire through the provided points. 

## Parameters

- `points`: a list of x,y points make up the polygon.
- `forConstruction = False`: should the new wires be reference geometry only?

## Examples

    from cqmore import Workplane

    triangle = Workplane().makePolygon(((-2, -2), (2, -2), (0, 2))) 

![makePolygon](images/workplane_makePolygon.JPG)

# `intersect2D`

Intersect the provided wire from the current wire. 

## Parameters

- `toIntersect`: a wire object, or a CQ object having a wire – object to intersect.

## Examples

    from cqmore import Workplane

    r1 = Workplane('YZ').rect(10, 10)
    r2 = Workplane('YZ').center(5, 5).rect(10, 10)
    intersected = r1.intersect2D(r2).extrude(1)

![intersect2D](images/workplane_intersect2D.JPG)

# `union2D`

Union the provided wire from the current wire. 

## Parameters

- `toUnion`: a wire object, or a CQ object having a wire – object to union.       

## Examples 

    from cqmore import Workplane

    r1 = Workplane('YZ').rect(10, 10)
    r2 = Workplane('YZ').center(5, 5).rect(10, 10)
    unioned = r1.union2D(r2).extrude(1)

![union2D](images/workplane_union2D.JPG)

# `cut2D`

Cut the provided wire from the current wire. 

## Parameters

- `toCut`: a wire object, or a CQ object having a wire – object to cut.       

## Examples 

    from cqmore import Workplane

    r1 = Workplane('YZ').rect(10, 10)
    r2 = Workplane('YZ').center(5, 5).rect(10, 10)
    cutted = r1.cut2D(r2).extrude(1)

![cut2D](images/workplane_cut2D.JPG)

# `hull2D`

Create a convex hull through the provided points. 

## Parameters

- `points = None`: a list of x, y points. If it's `None`, use all pending wires in the parent chain to create a convex hull.
- `forConstruction = False`: should the new wires be reference geometry only?

## Examples

    from random import random
    from cqmore import Workplane

    points = [(random(), random()) for i in range(20)]
    convex_hull = Workplane().hull2D(points)

    # an equivalent way
    # convex_hull = Workplane().polyline(points).close().hull2D()

![hull2D](images/workplane_hull2D.JPG)

# `polylineJoin2D`

Place a join on each point. Hull each pair of joins and union all convex hulls.

## Parameters

- `points`: a list of x, y points. 
- `join`: the wire as a join.
- `forConstruction = False`: should the new wires be reference geometry only?

## Examples 

    from cqmore import Workplane

    points = [(0, 0), (10, 10), (0, 15), (-10, 10), (-10, 0)]
    polyline = Workplane().polylineJoin2D(points, Workplane().polygon(6, 1))

![polylineJoin2D](images/workplane_polylineJoin2D.JPG)

# `splineApproxSurface`

Approximate a spline surface through the provided points.

## Parameters

- `points`: a 2D list of Vectors that represent the control points.
- `thickness = 0`: the amount of being thick (return 2D surface if 0).
- `combine = False`: should the results be combined with other solids on the stack (and each other)?
- `clean = True`: call `clean()` afterwards to have a clean shape.

## Examples 

    from cqmore import Workplane

    def paraboloid(x, y):
        return (x, y, ((y ** 2) - (x ** 2)) / 4)

    min_value = -30
    max_value = 30
    step = 5
    thickness = 0.5

    points = [[
            paraboloid(x / 10, y / 10) 
        for y in range(min_value, max_value + step, step)
    ] for x in range(min_value, max_value + step, step)]

    surface = Workplane().splineApproxSurface(points, thickness)

![splineApproxSurface](images/workplane_splineApproxSurface.JPG)

# `polyhedron`

Create any polyhedron with 3D points(vertices) and faces that enclose the solid. Each face contains the indices (0 based) of 3 or more points from the `points`.

## Parameters

- `points`: a list of 3D points(vertices).
- `faces`: face indices to fully enclose the solid. When looking at any face from the outside, the face must list all points in a counter-clockwise order.
- `combine = True`: should the results be combined with other solids on the stack (and each other)?
- `clean = True`: call `clean()` afterwards to have a clean shape.

## Examples 

    from cqmore import Workplane

    points = ((5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5))
    faces = ((0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3))
    tetrahedron = Workplane().polyhedron(points, faces)

![polyhedron](images/workplane_polyhedron.JPG)

# `hull`

Create a convex hull through the provided points. 

## Parameters

- `points = None`: a list of 3D points. If it's `None`, attempt to hull all of the items on the stack to create a convex hull.
- `combine = True`: should the results be combined with other solids on the stack (and each other)?
- `clean = True`: call `clean()` afterwards to have a clean shape.

## Examples

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

![hull](images/workplane_hull.JPG)


    from cqmore import Workplane
    from cqmore.polyhedron import uvSphere

    convex_hull = (Workplane()
                       .polyhedron(*uvSphere(10))
                       .box(20, 20, 5)
                       .hull()
                  )

![hull](images/workplane_hull2.JPG)

# `polylineJoin`

Place a join on each point. Hull each pair of joins and union all convex hulls.

## Parameters

- `points`: a list of points. 
- `join`: the sold as a join.
- `combine = True`: should the results be combined with other solids on the stack (and each other)?
- `clean = True`: call `clean()` afterwards to have a clean shape.

## Examples 

    from cqmore import Workplane

    polyline = (Workplane()
                    .polylineJoin(
                        [(0, 0, 0), (10, 0, 0), (10, 0, 10), (10, 10, 10)], 
                        Workplane().box(1, 1, 1)
                    )
                )

![polylineJoin](images/workplane_polylineJoin.JPG)