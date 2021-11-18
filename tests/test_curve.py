import unittest
from cqmore.curve import archimedeanSpiral, circle, helix, parametricEquation, sphericalSpiral, superellipse, superformula, torusKnot, logarithmicSpiral

class TestCurve(unittest.TestCase):
    def test_circle(self):
        self.assertEqual(
            (-1.0, 1.2246467991473532e-16), 
            circle(0.5, 1)
        )


    def test_logarithmicSpiral(self):
        self.assertEqual(
            (-2.6180342969327595, 3.2061673217966954e-16), 
            logarithmicSpiral(0.5)
        )


    def test_archimedeanSpiral(self):
        self.assertEqual(
            (-4.141592653589793, 5.071988186590933e-16), 
            archimedeanSpiral(0.5, 1, 1)
        )


    def test_superellipse(self):
        self.assertEqual(
            (-1.0, 6.081552622518829e-22), 
            superellipse(0.5, 1.5)
        )


    def test_superformula(self):
        self.assertEqual(
            (-1.851749424574581, 2.2677390056282136e-16), 
            superformula(0.5, 3, 4.5, 10, 10)
        )


    def test_helix(self):
        self.assertEqual(
            (1.0, -2.4492935982947064e-16, 1), 
            helix(1, 1, 1)
        )

    def test_sphericalSpiral(self):
        self.assertEqual(
            (-1.0, 6.123233995736766e-16, 6.123233995736766e-17), 
            sphericalSpiral(.5, 1, 10)
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
