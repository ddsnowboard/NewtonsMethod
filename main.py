import eqSolver
def newtonsMethod(eq, x, derivative=None):
	if not derivative:
		derivative = eq.derivative()
	return x-(eq.evaluate(x)/derivative.evaluate(x))
equation = eqSolver.Equation(input("What is the polynomial equation you want?"))
derivative = equation.derivative()
x_terms = [int(input("What x value should I start with?"))]
try:
	for i in range(int(input("How many times do you want to do the method? Or type nothing if you want to do it until it yields the answer"))):
		x_terms.append(newtonsMethod(equation, x_terms[-1], derivative))
	map(print, x_terms)
except ValueError:
	while True:
		x_terms.append(newtonsMethod(equation, x_terms[-1], derivative))
		if x_terms[-1] == x_terms[-2]:
			break