import unittest
import sys
sys.path.append('..')

from cqmore.curve import circle, helix, parametricEquation, torusKnot

class TestCurve(unittest.TestCase):
    def test_circle(self):
        self.assertEqual(
            (-1.0, 1.2246467991473532e-16), 
            circle(0.5, 1)
        )

    def test_helix(self):
        self.assertEqual(
            (1.0, -2.4492935982947064e-16, 1), 
            helix(1, 1, 1)
        )

    def test_torusKnot(self):
        self.assertEqual(
            (1.0, -2.4492935982947064e-16, -3.6739403974420594e-16), 
            torusKnot(0.5, 2, 3)
        )

    def test_parametricEquation(self):
        self.assertEqual(
            (1.0, -2.4492935982947064e-16, -3.6739403974420594e-16), 
            parametricEquation(torusKnot, p = 2, q = 3)(0.5)
        )

if __name__ == '__main__':
    unittest.main()
