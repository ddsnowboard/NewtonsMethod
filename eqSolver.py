import re
from collections import defaultdict
import math
def handleFraction(s):
		pattern = re.compile(r"(?P<top>[\d\.]+)[/](?P<bottom>[\d\.]+)")
		if not '/' in s:
			return float(s)
		elif s.count("/") > 1:
			raise ValueError()
		elif not pattern.match(s):
			return float(s)
		else:
			match = pattern.match(s)
			return float(match.group("top"))/ float(match.group("bottom"))
		return float(s)
def roundUp(i):
	if i%1 > 0:
		return int(i)+1
	return i
class Equation:
	def __init__(self, eq):	# y=2x^2-3x+5
		if type(eq) == type(""):
			self.regexes = {"normal" : re.compile(r"(?P<number>[\+-]?([\d\./])*)?[A-Za-z][\^](?P<exponent>[0-9/]+)"),
							"constant" : re.compile(r"^[\+-]?[\d]+$"), 
							"first" : re.compile(r"(?P<number>[\+-]?[\d\./]*)?[A-Za-z]")}						  
			self.coefficients = defaultdict(float)
			self.eq = re.subn(r"^y=|=y$", '', eq)[0]   # 2x^2-3x+5
			self.eq = self.eq.replace("**", "^").replace("+", " +").replace("-", ' -')  # 2x^2 -3x +5
			self.terms = self.eq.split(" ")	 # "2x^2", "-3x", "+5"
			self.terms = [i for i in self.terms if i != '']
			for i in self.terms:
				if self.regexes['constant'].match(i):
					self.coefficients[0] += handleFraction(i)  # "+5"
				elif self.regexes['normal'].match(i):
					match = self.regexes['normal'].match(i)
					if match.group("number") and match.group("number") != '+':
						if match.group("number") == "-":
							self.coefficients[handleFraction(match.group("exponent"))] -= 1
						else:
							self.coefficients[handleFraction(match.group("exponent"))] += handleFraction(match.group("number")) # '2'
					else:
						self.coefficients[handleFraction(match.group("exponent"))] += 1
				elif self.regexes["first"].match(i):
					match = self.regexes["first"].match(i)
					if match.group("number") and match.group("number") != "+":
						if match.group("number") == '-':
							self.coefficients[1] -= 1
						else:
							self.coefficients[1]+=handleFraction(match.group('number'))  	#"-3" 
					else:
						self.coefficients[1]+=1
		elif type(eq) == type({}):
			self.coefficients = defaultdict(float)
			for i, j in eq.items():
				self.coefficients[i] = j
		self.degree = 0
		for i, j in self.coefficients.items():
			if i > self.degree:
				self.degree = i
	def evaluate(self, x):
		end = 0
		for i, j in self.coefficients.items():
			end+=j*x**i
		return end
	def zero(self):
		if not self.degree == 2:
			raise Error("This isn't a quadratic!")
		else:
			a = self.coefficients[2]
			b = self.coefficients[1]
			c = self.coefficients[0]
			try:
				return ((-1*b+math.sqrt(b**2-4*a*c))/(2*a), (-1*b-math.sqrt(b**2-4*a*c))/(2*a))
			except ValueError:
				return None
	def intersect(self, other):
		if not type(other) == type(Equation("2x^2-4x+5")):
			raise Exception("You seem to have made a stupid; this is supposed to take another equation and find the intersection")
			return
		# Left will be variables; right will be constants. 
		# Left starts as self, right starts as other. 
		left = defaultdict(float)
		right = 0
		for i, j in self.coefficients.items():
			if i == 0:
				right-=j
			else:
				left[i]+=j
		for i, j in other.coefficients.items():
			if i == 0:
				right+=j
			else:
				left[i]-=j
		if self.degree == 0 and other.degree == 0:
			return right == 0
		elif self.degree<=1 and other.degree<=1:
			return (right/left[1], self.evaluate(right/left[1]))
		elif self.degree == 2 or other.degree == 2:
			return (((-1*left[1]+math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]), self.evaluate((-1*left[1]+math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]))), ((-1*left[1]-math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]), self.evaluate((-1*left[1]-math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]))))
		else:
			raise Error("I really can't get an accurate intersection with just this data.")
	def __str__(self):
		out = ""
		for i in range(roundUp(self.degree), -1, -1):
			if not self.coefficients[i] == 0:
				if i == 0:
					out += str(self.coefficients[i]) if self.coefficients[i] < 0 else ("+"+str(self.coefficients[i]))
				else:
					out += (("+" if self.coefficients[i] > 0 else "") + str(self.coefficients[i])+"x" + ("" if i == 1 else "^"+ str(i)))
		return out
	def derivative(self):
		new = {}
		for i, j in self.coefficients.items():
			new[i-1] = j*i if i != 0 else 0
		return Equation(new)
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
e = Equation("x^2+x+1")