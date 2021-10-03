import unittest
import sys
sys.path.append('..')

from math import cos, sin, radians

from cadquery import Workplane
from cqMore.operation2d import makePolygon

class Operation2DTestCase(unittest.TestCase):
    def test_makePolygon(self):
        fn = 12
        r = 5
        a_step = radians(360 / fn)

        points = [
            (r * cos(a_step * i), r * sin(a_step * i), 0) 
                for i in range(fn)
        ]

        polygon = makePolygon(Workplane(), points)

        actual = [vertex.toTuple() for vertex in polygon.vertices().vals()]
        self.assertListEqual(points, actual)
        
if __name__ == '__main__':
    unittest.main()
