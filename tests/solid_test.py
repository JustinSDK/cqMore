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

    def test_surface(self):
        points = [
            [(0, 1, 0), (10, 0, 0), (20, 0, 0)],
            [(0, 10, 0), (10, 10, 1), (21, 10, 0)],
            [(0, 20, 0), (10, 21, 0), (20, 20, 0)]
        ]

        sf = Workplane().surface(points, 1)

        self.assertEqual(32, sf.faces().size())

        vertices = sf.vertices()
        self.assertEqual(18, vertices.size())
        
if __name__ == '__main__':
    unittest.main()
