import unittest
import sys
sys.path.append('..')

from math import cos, sin, radians

from cadquery import Workplane, Wire, Vector
from cqMore.operation2d import makePolygon

class Operation2DTestCase(unittest.TestCase):
    def test_makePolygon(self):
        points = [
            (0, 0, 0), (10, 0, 0), (0, 10, 0), (-10, 0, 0)
        ]

        wire = Wire.makePolygon((
                 Vector(*p) for p in points + [points[0]]
            ), 
            False
        )

        expected = Workplane().rect(5, 5).eachpoint(lambda loc: wire.moved(loc)).vals()
        actual = makePolygon(Workplane().rect(5, 5), points).vals()
        for i in range(len(expected)):
            self.assertEqual(expected[i].geomType(), actual[i].geomType())
            self.assertEqual(expected[i].Center(), actual[i].Center())
            self.assertEqual(expected[i].Area(), actual[i].Area())
            self.assertEqual(expected[i].CenterOfBoundBox(), actual[i].CenterOfBoundBox())
            self.assertListEqual(
                [v.toTuple() for v in expected[i].Vertices()], 
                [v.toTuple() for v in actual[i].Vertices()]
            )
        
if __name__ == '__main__':
    unittest.main()
