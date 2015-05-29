import re
from collections import defaultdict
from collections import OrderedDict
import math
from fractions import Fraction
def roundUp(i):
	"""
	I'm sure this is unnecessary, but I apparently couldn't find a good way to
	do it in the standard library, so I have this.
	"""
	if i % 1 > 0:
		return int(i)+1
	return i
class ZeroError(Exception):
	pass
class Equation:
	"""
	This is an object that represents a polynomial equation.
	It isn't terribly extensible, so you have to be careful what
	you give it. It will take decimals and fractions as coefficients,
	and in exponents.
	"""
	def __init__(self, eq):	# y=2x^2-3x+5
	# If the equation is already a string, we have to turn it into an Equation
	# object.
		if type(eq) == type(""):
			eq = eq.replace(" ", "")
			# "normal" is an exponent greater than 1. "first" is an exponent of
			# 1.
			self.regexes = {"normal"   : re.compile(r"(?P<number>[\+-]?([\d\./])*)?[A-Za-z][\^](?P<exponent>[0-9/.]+)"),
							"constant" : re.compile(r"^[\+-]?[\d/^]+$"),
							"first"    : re.compile(r"(?P<number>[\+-]?[\d\./]*)?[A-Za-z]")}

			self.coefficients = defaultdict(float)
			self.eq = re.subn(r"^y=|=y$", '', eq)[0]   # 2x^2-3x+5
			# Add in spaces for later.
			self.eq = self.eq.replace("**", "^").replace("+", " +").replace("-", ' -')  # 2x^2 -3x +5
			self.terms = self.eq.split(" ")	 # "2x^2", "-3x", "+5"
			self.terms = [i for i in self.terms if i != '']
			for i in self.terms:
				if self.regexes['constant'].match(i):
					self.coefficients[0] += eval(i.replace("^", "**"))  # "+5"
				elif self.regexes['normal'].match(i):
					match = self.regexes['normal'].match(i)
					# If there is a number part on the term and it isn't just a
					# plus sign (either a minus sign or an actual number)
					if match.group("number") and match.group("number") != '+':
						if match.group("number") == "-":
							self.coefficients[Fraction(match.group("exponent"))] -= 1
						else:
							self.coefficients[Fraction(match.group("exponent"))] += Fraction(match.group("number"))
					else:
						# If the number is just a plus sign, make it one.
						self.coefficients[Fraction(match.group("exponent"))] += 1
				elif self.regexes["first"].match(i):
					match = self.regexes["first"].match(i)
					if match.group("number") and match.group("number") != "+":
						if match.group("number") == '-':
							self.coefficients[1] -= 1
						else:
							self.coefficients[1] += Fraction(match.group('number'))  	#"-3"
					else:
						self.coefficients[1] += 1
		elif type(eq) == type({}):
			# If our input is a dictionary, make that dictionary the coefficients
			# dictionary and be done.
			self.coefficients = defaultdict(float)
			for i, j in eq.items():
				self.coefficients[i] = j
		self.degree = max(self.coefficients.keys())
	def evaluate(self, x):
		"""
		This function simply evaluates the Equation. You cal also use
		the __call__ function (eqn(x)).
		It goes through the coefficients dictionary and adds up all the
		terms.
		"""
		end = 0
		for i, j in self.coefficients.items():
			try:
				end+=j*x**i
			except ZeroDivisionError:
				raise Exception("I had to divide by zero.")
		return end
	def zero(self):
		"""
		This will find the zero of a quadratic function using the quadratic
		equation.
		I could implement a way to find it numerically for other
		types, but maybe another time.
		"""
		if not self.isQuadratic():
			raise ZeroError("This function isn't quadratic")
		a = self.coefficients[2]
		b = self.coefficients[1]
		c = self.coefficients[0]
		try:
			return tuple(sorted(((-1 * b + math.sqrt(b**2 - 4 * a * c)) / (2 * a), (-1 * b - math.sqrt(b**2 - 4 * a * c)) / (2 * a))))
		except ValueError:
			return None
	def intersect(self, other):
		"""
		This function finds the intersection of two equations.
		It returns a tuple of the form (x, y), or a boolean if the functions are
		the same or will never intersect.
		"""
		if not type(other) == type(Equation("5")):
			raise Exception("Arguments {}, {} don't match Equation, Equation".format(type(self), type(other)))
			return
		# Left will be variables; right will be constants.
		# Left starts as self, right starts as other.
		left = defaultdict(float)
		right = 0
		# Go through the left hand function (self) and move all the constants to
		# the right and leave the variables on the left.
		for i, j in self.coefficients.items():
			if i == 0:
				right-=j
			else:
				left[i]+=j
		# Then do the same on the right.
		for i, j in other.coefficients.items():
			if i == 0:
				right+=j
			else:
				left[i]-=j
		if self.degree == 0 and other.degree == 0:
			return right == 0
		elif self.degree <= 1 and other.degree <= 1 :
			return (right/left[1], self.evaluate(right/left[1]))
		# Runs the quadratic equation if a degree is two. 
		elif self.degree == 2 or other.degree == 2:
			return (((-1*left[1]+math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]), self.evaluate((-1*left[1]+math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]))), ((-1*left[1]-math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]), self.evaluate((-1*left[1]-math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]))))
		else:
			raise Error("I really can't get an accurate intersection with just this data.")
	def __str__(self):
		out = ""
		sortedDict = OrderedDict(sorted(self.coefficients.items(), key=lambda x: -1*abs(x[0])))
		for degree, number in sortedDict.items():
			if number == 0:
				continue
			elif degree == 0:
				out+= ('+' if number > 0 else "") + str(number)
			elif number == 1 and degree == 1:
				out+= '+x'
			elif number == -1 and degree == 1:
				out += '-x'
			elif degree == 1:
				out += "{}{}x".format(('+' if number > 0 and degree != self.degree else ''), number)
			else:
				out+="{}{}x^{}".format(('+' if number > 0 and degree != self.degree else ""),str(number),str(degree))
		return out
	def derivative(self):
		new = {}
		for i, j in self.coefficients.items():
			new[i-1] = j*i if i != 0 else 0
		return Equation(new)
	def isQuadratic(self):
		POSSIBLE_DEGREES = [0, 1, 2]
		if self.degree != 2:
			return False
		for i in self.coefficients.keys():
			if not i in POSSIBLE_DEGREES:
				return False
		return True
	def __eq__(self, other):
		if self.degree == other.degree:
			if self.coefficients == other.coefficients:
				return True
		return False
	def __ne__(self, other):
		return not self.__eq__(self, other)
	def __bool__(self, other):
		return self == Equation("0")
	def __getitem__(self, key):
		return self.coefficients[key]
	def __setitem__(self, key, value):
		self.coefficients[key] = value
	def __call__(self, x):
		return self.evaluate(x)
