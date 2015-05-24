import pprint
import eqSolver
from time import clock
def oneIteration(eq, x, derivative=None):
	if derivative is None:
		derivative = eq.derivative()
	return x-(eq.evaluate(x)/derivative.evaluate(x))
def newtonsMethod(*, eqn, x_terms, initial_x):
	derivative = eqn.derivative()
	output = [initial_x]
	if x_terms:
		for i in range(x_terms):
			output.append(oneIteration(eqn, output[-1], derivative))
		return output
	else:
		clock()
		while True:
			output.append(oneIteration(eqn, output[-1], derivative))
			if output[-1] == output[-2]:
				return output
			elif clock() > 10:
				return output
if __name__ == "__main__":
	eqn = eqSolver.Equation((input("What is the polynomial equation you want? ")))
	try:
		x_terms = int(input("How many times do you want to do the method? Or type nothing if you want to do it until it yields the answer. "))
	except ValueError:
		x_terms = None
	initial_x = int(input("What x value should I start with?\n"))
	print(newtonsMethod(eqn=eqn, x_terms=x_terms, initial_x=initial_x)[-10:])
	input()
