import unittest
from typing import cast
import sys
sys.path.append('..')

from cadquery import Vertex
from cqMore import Workplane

class SolidTestCase(unittest.TestCase):
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

        actual = cast(list[Vertex], vertices.vals())
        self.assertListEqual(
            sorted(points), 
            sorted([v.toTuple() for v in actual])
        )
        
if __name__ == '__main__':
    unittest.main()
