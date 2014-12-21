import eqSolver
import pprint
from time import clock
def newtonsMethod(eq, x, derivative=None):
	if derivative is None:
		derivative = eq.derivative()
	return x-(eq.evaluate(x)/derivative.evaluate(x))
equation = eqSolver.Equation(input("What is the polynomial equation you want?"))
derivative = equation.derivative()
while True:
	try:
		x_terms = [int(input("What x value should I start with?"))]
		break
	except ValueError:
		print("That's not a number!")
try:
	for i in range(int(input("How many times do you want to do the method? Or type nothing if you want to do it until it yields the answer"))):
		x_terms.append(newtonsMethod(equation, x_terms[-1], derivative))
except ValueError:
	clock()
	while True:
		x_terms.append(newtonsMethod(equation, x_terms[-1], derivative))
		if x_terms[-1] == x_terms[-2]:
			break
		elif clock() > 10:
			print("I couldn't find a root after {} tries".format(len(x_terms)))
			pprint.PrettyPrinter().pprint(x_terms[-10:])
			input()
			exit()
pprint.PrettyPrinter().pprint(x_terms)
print("The result is {}".format(x_terms[-1]))
input()