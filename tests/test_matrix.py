import unittest
import sys
sys.path.append('..')

from cqmore.matrix import Matrix3D

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


if __name__ == '__main__':
    unittest.main()
