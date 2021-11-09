from typing import Iterable, Union, overload

import cadquery
from cadquery import Wire, Shape, Compound, Solid
from cadquery.cq import T, VectorLike

from ._typing import FaceIndices, MeshGrid
from ._solid import makePolyhedron, polylineJoin, splineApproxSurface
from ._wire import bool2D, makePolygon, polylineJoinWire
from .polygon import hull2D
from .polyhedron import hull


class Workplane(cadquery.Workplane):
    """
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

    """

    def makePolygon(self: T, points: Iterable[VectorLike], forConstruction: bool = False) -> T:
        """
        Make a multiple sided wire through the provided points. 
        
        ## Parameters

        - `points`: a list of x, y points comprise the polygon.
        - `forConstruction`: should the new wires be reference geometry only?
        
        ## Examples
        
            from cqmore import Workplane

            triangle = Workplane().makePolygon(((-2, -2), (2, -2), (0, 2))) 

        """

        p = makePolygon(points, forConstruction)
        return self.eachpoint(lambda loc: p.moved(loc), True)


    def intersect2D(self: T, toIntersect: Union[T, Wire]) -> T:
        """
        Intersect the provided wire from the current wire. 

        ## Parameters

        - `toIntersect`: a wire object, or a CQ object having a wire – object to intersect.

        ## Examples

            from cqmore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            intersected = r1.intersect2D(r2).extrude(1)

        """

        return bool2D(self, toIntersect, 'intersect')
        

    def union2D(self: T, toUnion: Union[T, Wire]) -> T:
        """
        Union the provided wire from the current wire. 

        ## Parameters

        - `toUnion`: a wire object, or a CQ object having a wire – object to union.       

        ## Examples 

            from cqmore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            unioned = r1.union2D(r2).extrude(1)

        """

        return bool2D(self, toUnion, 'union')


    def cut2D(self: T, toCut: Union[T, Wire]) -> T:
        """
        Cut the provided wire from the current wire. 

        ## Parameters

        - `toCut`: a wire object, or a CQ object having a wire – object to cut.       

        ## Examples 

            from cqmore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            cutted = r1.cut2D(r2).extrude(1)

        """

        return bool2D(self, toCut, 'cut')

    @overload
    def hull2D(self: T) -> T:
        ...

    @overload
    def hull2D(self: T, points: Iterable[VectorLike] = ..., forConstruction: bool = ...) -> T:
        ...

    def hull2D(self: T, points = None, forConstruction = False) -> T:
        """
        Create a convex hull through the provided points.

        ## Parameters

        - `points`: a list of x, y points. If it's `None`, use all pending wires 
                    in the parent chain to create a convex hull.
        - `forConstruction`: should the new wires be reference geometry only?

        ## Examples 

            from random import random
            from cqmore import Workplane

            points = [(random(), random()) for i in range(20)]
            convex_hull = Workplane().hull2D(points)
            
            # an equivalent way
            # convex_hull = Workplane().polyline(points).close().hull2D()

        """

        if points:
            p = makePolygon(hull2D(points), forConstruction)
            return self.eachpoint(lambda loc: p.moved(loc), True)

        wires = self.ctx.popPendingWires()
        
        p = makePolygon(hull2D(v.toTuple() for wire in wires for v in wire.Vertices()), forConstruction)
        moved = self.eachpoint(lambda loc: p.moved(loc), True)
        return self.newObject([o for o in moved.objects if not (o in wires)])


    def polylineJoin2D(self: T, points: Iterable[VectorLike], join: Union[T, Wire], forConstruction: bool = False) -> T:
        """
        Place a join on each point. Hull each pair of joins and union all convex hulls.

        ## Parameters

        - `points`: a list of x, y points. 
        - `join`: the wire as a join.
        - `forConstruction`: should the new wires be reference geometry only?

        ## Examples 

            from cqmore import Workplane

            points = [(0, 0), (10, 10), (0, 15), (-10, 10), (-10, 0)]
            polyline = Workplane().polylineJoin2D(points, Workplane().polygon(6, 1))

        """       

        polyline = polylineJoinWire(points, join, forConstruction)
        return self.eachpoint(lambda loc: polyline.moved(loc), True)


    def splineApproxSurface(self: T, points: MeshGrid, thickness: float = 0, combine: bool = True, clean: bool = True) -> T:    
        """
        Approximate a spline surface through the provided points.

        ## Parameters

        - `points`: a 2D list of Vectors that represent the control points.
        - `thickness`: the amount of being thick (return 2D surface if 0).
        - `combine`: should the results be combined with other solids on the stack (and each other)?
        - `clean`: call `clean()` afterwards to have a clean shape.

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

        """

        return _solid_each_combine_clean(self, splineApproxSurface(points, thickness), combine, clean)


    def polyhedron(self: T, points: Iterable[VectorLike], faces: Iterable[FaceIndices], combine: bool = True, clean: bool = True) -> T:
        """
        Create any polyhedron with 3D points(vertices) and faces that enclose the solid. 
        Each face contains the indices (0 based) of 3 or more points from the `points`.

        ## Parameters

        - `points`: a list of 3D points(vertices).
        - `faces`: face indices to fully enclose the solid. When looking at any face from 
                   the outside, the face must list all points in a counter-clockwise order.
        - `combine`: should the results be combined with other solids on the stack (and each other)?
        - `clean`: call `clean()` afterwards to have a clean shape.

        ## Examples 

            from cqmore import Workplane

            points = ((5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5))
            faces = ((0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3))
            tetrahedron = Workplane().polyhedron(points, faces)
        
        """

        return _solid_each_combine_clean(self, makePolyhedron(points, faces), combine, clean)


    @overload
    def hull(self: T) -> T:
        ...

    @overload
    def hull(self: T, points: Iterable[VectorLike] = ..., combine: bool = ..., clean: bool = ...) -> T:
        ...

    def hull(self: T, points = None, combine = True, clean = True) -> T:
        """
        Create a convex hull through the provided points. 

        ## Parameters

        - `points`: a list of 3D points. If it's `None`, attempt to hull all of the items on the stack 
                    to create a convex hull.
        - `combine`: should the results be combined with other solids on the stack (and each other)?
        - `clean`: call `clean()` afterwards to have a clean shape.

        ## Examples 

            # ex1

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

            # ex2

                from cqmore import Workplane
                from cqmore.polyhedron import uvSphere

                convex_hull = (Workplane()
                                  .polyhedron(*uvSphere(10))
                                  .box(20, 20, 5)
                                  .hull()
                              )

        """

        if points:
            pts = points
        else:
            items: Iterable[Shape] = (o for o in self.objects if isinstance(o, Shape))
            pts = (v.toTuple() 
                for shape in items
                    for v in shape.Vertices()
            )

        return _solid_each_combine_clean(self, makePolyhedron(*hull(pts)), combine, clean)
    

    def polylineJoin(self: T, points: Iterable[VectorLike], join: Union[T, Solid, Compound], combine: bool = False, clean: bool = True) -> T:
        """
        Place a join on each point. Hull each pair of joins and union all convex hulls.

        ## Parameters

        - `points`: a list of points. 
        - `join`: the sold as a join.
        - `combine`: should the results be combined with other solids on the stack (and each other)?
        - `clean`: call `clean()` afterwards to have a clean shape.

        ## Examples 

            from cqmore import Workplane

            polyline = (Workplane()
                            .polylineJoin(
                                [(0, 0, 0), (10, 0, 0), (10, 0, 10), (10, 10, 10)], 
                                Workplane().box(1, 1, 1)
                            )
                        )

        """       

        return _solid_each_combine_clean(self, polylineJoin(points, join), combine, clean)


def _solid_each_combine_clean(workplane, solid, combine, clean):
    all = workplane.eachpoint(lambda loc: solid.moved(loc), True)
    if not combine:
        return all
    else:
        return workplane.union(all, clean=clean)


def extend(workplaneClz):
    """
    Extend `cadquery.Workplane`.

    ## Parameters

    - `workplaneClz`: `cadquery.Workplane`.

    ## Examples 

        from cadquery import Workplane
        import cqmore
        cqmore.extend(Workplane)

    """

    for attr in dir(Workplane):
        if not attr.startswith('__'):
            setattr(workplaneClz, attr, getattr(Workplane, attr))
    return workplaneClz
