import unittest
from typing import cast
import sys
sys.path.append('..')

from math import cos, sin, radians

from cadquery import Wire, Vector
from cqMore import Workplane

class WireTestCase(unittest.TestCase):
    def test_makePolygon(self):
        points = [
            (0, 0, 0), (10, 0, 0), (0, 10, 0), (-10, 0, 0)
        ]

        wire = Wire.makePolygon((
                 Vector(*p) for p in points + [points[0]]
            ), 
            False
        )

        expected = cast(list[Wire], Workplane().rect(5, 5).eachpoint(lambda loc: wire.moved(loc)).vals())
        actual = cast(list[Wire], Workplane().rect(5, 5).makePolygon(points).vals())
        for i in range(len(expected)):
            self.assertWireEqual(expected[i], actual[i])

    def test_intersect2D(self):
        r1 = Workplane().rect(10, 10)
        r2 = Workplane().center(5, 5).rect(10, 10)
        
        expected = cast(Wire, Workplane().center(2.5, 2.5).rect(5, 5).val())
        actual = cast(Wire, r1.intersect2D(r2).val())

        self.assertWireEqual(expected, actual)

    def test_union2D(self):
        r1 = Workplane().rect(10, 10)
        r2 = Workplane().center(5, 5).rect(10, 10)
        
        expected = cast(Wire, Workplane().polyline([
            (-5, -5), (5, -5), (5, 0), (10, 0), (10, 10), (0, 10), (0, 5), (-5, 5)]).close().val()
        )
        actual = cast(Wire, r1.union2D(r2).val())

        self.assertWireEqual(expected, actual)        

    def assertWireEqual(self, expected, actual):
        self.assertEqual(expected.geomType(), actual.geomType())
        self.assertEqual(expected.Center(), actual.Center())
        self.assertEqual(expected.Area(), actual.Area())
        self.assertEqual(expected.CenterOfBoundBox(), actual.CenterOfBoundBox())
        self.assertListEqual(
            sorted([v.toTuple() for v in expected.Vertices()]), 
            sorted([v.toTuple() for v in actual.Vertices()])
        )

if __name__ == '__main__':
    unittest.main()
