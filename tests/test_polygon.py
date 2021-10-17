import unittest
import sys
sys.path.append('..')

from cqmore.polygon import regularPolygon, hull2D

class TestPolygon(unittest.TestCase):
    def test_regularPolygon(self):
        polygon = regularPolygon(nSides = 6, radius = 10)
        self.assertEqual(6, len(polygon))

        polygon = regularPolygon(
            nSides = 6, 
            radius = 10, 
            thetaStart = 45, 
            thetaEnd = 270
        )
        self.assertEqual(8, len(polygon))


    def test_hull2D(self):
        points = [
            (0.855355763576732, 0.16864474737612778), 
            (0.7653639827409133, 0.21243642222244463), 
            (0.9956528164357294, 0.6119951986040002), 
            (0.34997550432063895, 0.1878314178942282), 
            (0.5811634308956635, 0.8646520280492559), 
            (0.4556958318174945, 0.16723661322362438), 
            (0.9398877210188867, 0.2413165664583884), 
            (0.375900956434601, 0.09820967766941846), 
            (0.8532633331060003, 0.5955415267257996)
        ]

        self.assertEqual(6, len(hull2D(points)))


if __name__ == '__main__':
    unittest.main()
