import unittest
import NewtonsMethod, eqSolver

class EquationSolverTest(unittest.TestCase):
    def test_RoundUp(self):
        """
        This tests the roundUp() function
        """
        self.assertEqual(eqSolver.roundUp(1.001), 2)
        self.assertEqual(eqSolver.roundUp(81.999), 82)
        self.assertEqual(eqSolver.roundUp(100.000001), 101)
    def test_ZeroDegree(self):
        """
        This makes sure that a zeroth-degree function runs properly.
        It didn't used to, so I thought I should have this test to make sure.
        """
        eqn = eqSolver.Equation("5^2")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), 5**2)
    def test_NormalEqn(self):
        """
        This should test for pretty much normal equations
        """
        eqn = eqSolver.Equation("x^2-5x+5")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), i**2-5*i+5)
    def test_Fractions(self):
        """
        This makes sure that the fraction functionality works.
        It took some extra logic, and I want to make sure that it is always right.
        """
        eqn = eqSolver.Equation("1/2x^2-5/8x+105/2")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), .5 * i ** 2 - 5 / 8 * i + 105 / 2)
    def test_FractionalExponents(self):
        """
        This tests if fractional exponents work. They don't by default, and I
        want to make sure that the extra code I included to make them work is
        right.
        """
        eqn = eqSolver.Equation("2x^1.5+x^1/2-x^5/3")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), 2 * i ** 1.5 + i ** .5 - i ** (5/3))
        eqn = eqSolver.Equation("1/2x^5/8")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn(i), .5 * i ** (5 / 8))
    def test_Spaces(self):
        """
        I needed to make sure that spaces are handled properly.
        """
        eqn = eqSolver.Equation("y = 2 x ^2 /  3- 23x   ^4- 3 3 x^4")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertAlmostEqual(eqn(i), 2 * i ** (2/3) - 23 * i ** 4 - 33 * i ** 4, delta=1) # The numbers are too big, so I have to use assertAlmostEqual.
    def test_Degree(self):
        """
        Makes sure that the degree counting functionality works.
        """
        s = ""
        for i in range(1, 50):
           with self.subTest():
               s += "+2x^{}".format(i)
               self.assertEqual(eqSolver.Equation(s).degree, i)
    def test_Dictionary(self):
        """
        Makes sure that the Equation constructor takes a dictionary properly.
        """
        d = {2:2, 1:-5, 0:3}
        eqn = eqSolver.Equation(d)
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn(i), 2*i**2-5*i+3)
    def test_Zero(self):
        """
        Checks some things on the Equation.zero() function.
        """
        eqns = [(eqSolver.Equation("x^2-6x+9"),(3.0, 3.0)), (eqSolver.Equation("x^2"), (0.0, 0.0)), (eqSolver.Equation("x^2-2x-15"), (-3.0, 5.0)), (eqSolver.Equation("x^2+x+15"), None)]
        for i, j in eqns:
            with self.subTest(equation=i):
                self.assertEqual(i.zero(), j)
        eq = eqSolver.Equation("5x")
        with self.subTest(equation=eq):
            with self.assertRaises(eqSolver.ZeroError):
                eq.zero()
        eq = eqSolver.Equation("x^2-2x^.5+4x")
        with self.subTest(equation=eq):
            with self.assertRaises(eqSolver.ZeroError):
                print(eq.zero())
    def test_input_checking(self):
        """
        Makes sure the input checking on NewtonsMethod works
        right
        """
        s = [("2x^2-5x+5=y",True), ("2x^2-5x+4", True), ("5z-5x^4+3",False), ("2x-5=t", False)]
        for i, j in s:
            with self.subTest(s=i):
                self.assertEqual(eqSolver.Equation.inputCheck(i), j)
    def test_number_check(self):
        """
        Makes sure that the function that checks that the inputs for
        initial x and number of runs are numbers
        """
        s = [("2", True), ("a", False), ("23", True), ("2a", False), ("", True)]
        for i, j in s:
            with self.subTest(string=i):
                self.assertEqual(bool(eqSolver.Equation.numberCheck(i)), j)

if __name__ == "__main__":
    unittest.main()
