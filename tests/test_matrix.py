import unittest
import sys
sys.path.append('..')

from cqmore.matrix import Matrix3D, identity, scaling
from cqmore.polyhedron import uvSphere

class TestMatrix(unittest.TestCase):
    def test_Matrix3D(self):
        m = [
            [1, 0, 0, 5],
            [0, 1, 0, 5],
            [0, 0, 1, 5],
            [0, 0, 0, 1]
        ]
        m3d = Matrix3D(m)     

        self.assertListEqual(m, m3d.wrapped.tolist())


    def test_transform(self):
        translation = Matrix3D([
            [1, 0, 0, 5],
            [0, 1, 0, 5],
            [0, 0, 1, 5],
            [0, 0, 0, 1]
        ])

        translated = translation.transform((10, 20, 30)) 
        self.assertEqual((15, 25, 35), translated)


    def test_transformAll(self):
        translation = Matrix3D([
            [1, 0, 0, 5],
            [0, 1, 0, 5],
            [0, 0, 1, 5],
            [0, 0, 0, 1]
        ])

        points = [(10, 20, 30), (0, 0, 0), (-10, -20, -30)]
        translated = translation.transformAll(points) 
        self.assertTupleEqual(((15, 25, 35), (5, 5, 5), (-5, -15, -25)), translated)


    def test_identity(self):
        m = identity()
        self.assertListEqual([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], m.wrapped.tolist())


    def test_scaling(self):
        sphere = uvSphere(1)
        m = scaling((2, 1, 1)) 
        scaled_points = m.transformAll(sphere.points)
        
        expected = ((2.0, 0.0, 6.123233995736766e-17), (-0.9999999999999996, 0.8660254037844387, 6.123233995736766e-17), (-1.0000000000000009, -0.8660254037844385, 6.123233995736766e-17), (0, 0, -1), (0, 0, 1))
        self.assertTupleEqual(expected, scaled_points)
        

if __name__ == '__main__':
    unittest.main()
