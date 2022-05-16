import unittest
from typing import cast, List
from cadquery import Vector, Vertex, Wire
from cqmore import Workplane

class TestWorkplane2D(unittest.TestCase):
    def test_makePolygon(self):
        points = (
            (0, 0, 0), (10, 0, 0), (0, 10, 0), (-10, 0, 0)
        )

        wire = Wire.makePolygon((
                 Vector(*p) for p in points + (points[0], )
            ), 
            False
        )

        expected = cast(List[Wire], 
                        Workplane().rect(5, 5, forConstruction = True)
                                   .vertices()
                                   .eachpoint(lambda loc: wire.moved(loc))
                                   .vals()
                   )
        actual = cast(List[Wire], 
                      Workplane().rect(5, 5, forConstruction = True)
                                 .vertices()
                                 .makePolygon(points)
                                 .vals()
                 )
        for i in range(len(expected)):
            self.assertWireEqual(expected[i], actual[i])


    def test_intersect2D(self):
        r1 = Workplane().rect(10, 10)
        r2 = Workplane().center(5, 5).rect(10, 10)
        
        expected = cast(Wire, Workplane().center(2.5, 2.5).rect(5, 5).val())
        actual = cast(Wire, r1.intersect2D(r2).val())
        self.assertWireEqual(expected, actual)

        wire = cast(Wire, r2.val())
        actual = cast(Wire, r1.intersect2D(wire).val())
        self.assertWireEqual(expected, actual)


    def test_union2D(self):
        r1 = Workplane().rect(10, 10)
        r2 = Workplane().center(5, 5).rect(10, 10)
        
        expected = cast(Wire, Workplane().polyline(
            ((-5, -5), (5, -5), (5, 0), (10, 0), (10, 10), (0, 10), (0, 5), (-5, 5))).close().val()
        )
        actual = cast(Wire, r1.union2D(r2).val())
        self.assertWireEqual(expected, actual)       

        wire = cast(Wire, r2.val())
        actual = cast(Wire, r1.union2D(wire).val())
        self.assertWireEqual(expected, actual)         


    def test_cut2D(self):
        r1 = Workplane().rect(10, 10)
        r2 = Workplane().center(5, 5).rect(10, 10)
        
        expected = cast(Wire, Workplane().polyline(
            ((-5, -5), (5, -5), (5, 0), (0, 0), (0, 5), (-5, 5))).close().val()
        )
        actual = cast(Wire, r1.cut2D(r2).val())
        self.assertWireEqual(expected, actual)     

        wire = cast(Wire, r2.val())
        actual = cast(Wire, r1.cut2D(wire).val())
        self.assertWireEqual(expected, actual)       


    def test_hull2D(self):
        points = (
            (0.855355763576732, 0.16864474737612778), 
            (0.7653639827409133, 0.21243642222244463), 
            (0.9956528164357294, 0.6119951986040002), 
            (0.34997550432063895, 0.1878314178942282), 
            (0.5811634308956635, 0.8646520280492559), 
            (0.4556958318174945, 0.16723661322362438), 
            (0.9398877210188867, 0.2413165664583884), 
            (0.375900956434601, 0.09820967766941846), 
            (0.8532633331060003, 0.5955415267257996)
        )

        pts = Workplane().hull2D(points, forConstruction = True).vertices().vals()
        self.assertEqual(6, len(pts))


    def test_polylineJoin2D(self):
        points = ((0, 0), (10, 10), (0, 15), (-10, 10), (-10, 0))
        polyline = Workplane().polylineJoin2D(points, Workplane().polygon(6, 1))
        self.assertEqual(18, len(polyline.vertices().vals()))


    def assertWireEqual(self, expected, actual):
        self.assertEqual(expected.geomType(), actual.geomType())
        self.assertEqual(expected.Center(), actual.Center())
        self.assertEqual(expected.Area(), actual.Area())
        self.assertEqual(expected.CenterOfBoundBox(), actual.CenterOfBoundBox())
        self.assertListEqual(
            sorted([v.toTuple() for v in expected.Vertices()]), 
            sorted([v.toTuple() for v in actual.Vertices()])
        )

class TestWorkplane3D(unittest.TestCase):
    def test_splineApproxSurface(self):
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
        self.assertEqual(6, surface.faces().size())


    def test_polyhedron(self):
        points = (
            (5, -5, -5), (-5, 5, -5), (5, 5, 5), (-5, -5, 5)
        )

        faces = (
            (0, 1, 2), (0, 3, 1), (1, 3, 2), (0, 2, 3)
        )

        tetrahedron = Workplane().polyhedron(points, faces)
        self.assertEqual(4, tetrahedron.faces().size())

        vertices = tetrahedron.vertices()
        self.assertEqual(4, vertices.size())

        actual = cast(List[Vertex], vertices.vals())
        self.assertListEqual(
            sorted(points), 
            sorted([v.toTuple() for v in actual])
        )


    def test_hull(self):
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

        self.assertEqual(10, len(convex_hull.faces().vals()))
        self.assertEqual(7, len(convex_hull.vertices().vals()))


    def test_polylineJoin(self):
        polyline = (Workplane()
                        .polylineJoin(
                            [(0, 0, 0), (10, 0, 0), (10, 0, 10), (10, 10, 10)], 
                            Workplane().box(1, 1, 1)
                        )
                    )
        self.assertEqual(16, len(polyline.vertices().vals()))


if __name__ == '__main__':
    unittest.main()
