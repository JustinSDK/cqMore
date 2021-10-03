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
            (r * cos(a_step * i), r * sin(a_step * i)) 
                for i in range(fn)
        ]

        polygon = makePolygon(Workplane(), points)
        
        vectors = (vertex.Center() for vertex in polygon.vertices().vals())
        actual = [(vector.x, vector.y) for vector in vectors]
        self.assertListEqual(points, actual)
        
if __name__ == '__main__':
    unittest.main()
