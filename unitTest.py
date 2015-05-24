import unittest
import NewtonsMethod, eqSolver

class EquationSolverTest(unittest.TestCase):
    def test_ZeroDegree(self):
        eqn = eqSolver.Equation("5^2")
        for i in range(1, 1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), 5**2)
    def test_NormalEqn(self):
        eqn = eqSolver.Equation("x^2-5x+5")
        for i in range(1, 1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), i**2-5*i+5)
if __name__ == "__main__":
    unittest.main()
    input()
