from .wire import (
    makePolygon,
    bool2D
)

from .solid import (
    polyhedron,
    surface
)

from typing import (
    Iterable,
    Union
)

from .cq_typing import (
    T,
    VectorLike,
    FaceIndices,
    MeshGrid
)

from cadquery import (
    Wire
)

import cadquery

class Workplane(cadquery.Workplane):
    """
    Define plugins. You may simply use `cqMore.Workplane` to replace `cadquery.Workplane`. For example:

        from cqMore import Workplane

        result = (Workplane()
                    .rect(10, 10)
                    .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2))).extrude(1)
                 )

    You may also attach methods of `cqMore.Workplane` to `cadquery.Workplane`, such as:

        from cadquery import Workplane
        import cqMore

        Workplane.makePolygon = cqMore.Workplane.makePolygon

        result = (Workplane()
                    .rect(10, 10)
                    .makePolygon(((-2, -2), (2, -2), (2, 2), (-2, 2))).extrude(1)
                 )

    """

    def makePolygon(self: T, points: Iterable[VectorLike], forConstruction: bool = False) -> T:
        """
        Make a multiple sided wire from `points`. 
        
        ## Parameters

        - `points`: the list of x,y points of the polygon.
        - `forConstruction`: should the new wires be reference geometry only?
        
        ## Examples
        
            from cqMore import Workplane

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

            from cqMore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            intersected = r1.intersect2D(r2)

        """

        return bool2D(self, toIntersect, 'intersect')
        
    def union2D(self: T, toUnion: Union[T, Wire]) -> T:
        """
        Union the provided wire from the current wire. 

        ## Parameters

        - `toUnion`: a wire object, or a CQ object having a wire – object to union.       

        ## Examples 

            from cqMore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            unioned = r1.union2D(r2)

        """

        return bool2D(self, toUnion, 'union')

    def cut2D(self: T, toCut: Union[T, Wire]) -> T:
        """
        Cut the provided wire from the current wire. 

        ## Parameters

        - `toCut`: a wire object, or a CQ object having a wire – object to cut.       

        ## Examples 

            from cqMore import Workplane

            r1 = Workplane('YZ').rect(10, 10)
            r2 = Workplane('YZ').center(5, 5).rect(10, 10)
            cutted = r1.cut2D(r2)

        """

        return bool2D(self, toCut, 'cut')

    def polyhedron(self: T, points: Iterable[VectorLike], faces: Iterable[FaceIndices], combine: bool = True, clean: bool = True) -> T:
        """
        create any polyhedron with 3D points(vertices) and faces that enclose the solid. 
        Each face contains the indices (0 based) of 3 or more points from the `points`.

        ## Parameters

        - `points`: a list of 3D points(vertices).
        - `faces`: face indices to fully enclose the solid. When looking at any face from 
                   the outside, the face must list all points in a counter-clockwise order.

        ## Examples 

            from cqMore import Workplane

            points = ((5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5))
            faces = ((0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3))
            tetrahedron = Workplane().polyhedron(points, faces)
        
        """

        poly = polyhedron(points, faces)
        poly_all = self.eachpoint(lambda loc: poly.moved(loc), True)
        
        if not combine:
            return poly_all
        else:
            return self.union(poly_all, clean=clean)

    def surface(self: T, points: MeshGrid, thickness: float, combine: bool = True, clean: bool = True) -> T:
        """
        create a surface with a coordinate meshgrid.

        ## Parameters

        - `points`: a coordinate meshgrid.
        - `thickness`: the amount of being thick.
        - `combine`: should the results be combined with other solids on the stack (and each other)?
        - `clean`: call `clean()` afterwards to have a clean shape.

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

        """

        sf = surface(points, thickness)
        sf_all = self.eachpoint(lambda loc: sf.moved(loc), True)
        
        if not combine:
            return sf_all
        else:
            return self.union(sf_all, clean=clean)

