# default version
def factorial(n):
		if not n:
				return 1
		else:
				return n * factorial(n - 1)

factorial(5)


def create_factorial():
		def factorial(n):
				if not n:
						return 1
				else:
						return n * create_factorial()(n - 1)
		return factorial

factorial = create_factorial()

factorial(5)

def create_factorial(c):
		def factorial(n):
				if not n:
						return 1
				else:
						return n * c(c)(n - 1)
		return factorial

factorial = create_factorial(create_factorial)

# create anything

def create_anything(c, f):
		def anything(x):
				return c(c, f)(x)
		return f(anything)


def _factorial(c):
		def factorial(n):
				if not n:
						return 1
				else:
						return n * c(n - 1)
		return factorial

factorial = create_anything(create_anything, _factorial)

# single argument

def create(f):
		def create_anything(c):
				def anything(x):
						return c(c)(x)
				return f(anything)
		return create_anything(create_anything)

factorial = create(_factorial)

# fuck up all the variable names.

def _f(f):
		def _c(c):
				def _x(x):
						return c(c)(x)
				return f(_x)
		return _c(_c)

# now use auto call because we can't lambaste _c(_c)

def _f(f):
		def _autocall(x):
				return x(x)
		def _c(c):
				def _x(x):
						return c(c)(x)
				return f(_x)
		return _autocall(_c)

# fuck up the names some more
def _f(f):
		def _x(x):
				return x(x)
		def _y(y):
				def _v(v):
						return y(y)(v)
				return f(_v)
		return _x(_y)


# compress _f down into lambdas, we get...

Y = lambda f: (lambda x: x(x))(lambda y: f(lambda v: y(y)(v)))

# now to unwind with auto call

def ac(x):
	return x(x)

Y = lambda f: ac(lambda y: f(lambda v: y(y)(v)))
# y is create_anything. v is x
# lambda y: f(lambda v: y(y)(v)) is create_anything
# f(lambda v: y(y)(v)) is anything
# now unwind the other lambdas

def YC(f):
		def create_anything(c):
				def anything(x):
						return c(c)(x)
				return f(anything)
		return ac(create_anything)

# add debugging shit

from traceback import print_exc

def _factorial(c):
	print "_factorial c is %s"%c
	def factorial(n):
		if not n:
			return 1
		else:
			return n * c(n - 1)
	return factorial

"""
the type of factorial is int -> int
type of _factorial is (Something -> (int -> int)) ->(int -> int)

"""

def YC(f):
	def create_what_outside_has(c):
		# c is create_anything itself. it is being provided by autocall
		# we need to pass it to itself so it can wrap it in a lambda for the next layer
		# the c argument. because its passe don the stack, we can use it for layer2+ calls
		def the_recursive_call(x):
			# x is the number being computed on
			c_of_c = c(c) # c of c is factorial, from inside of _factorial
			# note this c(c) is legal because c is a functional argument
			print "c_of_c=%s"%(c_of_c)
			return c_of_c(x)
		r = f(the_recursive_call)
		return r
	return ac(create_what_outside_has)

# YC has type ((int -> int) -> (int -> int))
# ac has type (X -> foo) -> foo
# the recursive call has type foo -> (int -> int)
# c_of_c has type

YC(_factorial)(5)

"""
YC takes in a function f. It first constructs create_what_outside has and (implicitly, through currying) pass it f
create_what_outside_has takes in an argument, which will be itself (provided by auto call!)
create_what outside has defines a function anything.
Anything computes c(c). c is available because it was the argument to create_what_outside_has, and create_what_outside_has has itself has an argument. so c(c) is create_what_outside_has(create_what_outside_has). Recall we are calling this from (2 layers) inside create_what_outside_has, so its recursive!
anything, so anything=create_what_outside_has(create_what_outside_has) is called on x, which is really n-1 provided by _f
then we construct r by calling f on anything. recall that f(anything) will return a function
_f. _f will check for the base case. and if its not the base case it will call anything(n-1)
so anything just does what the recursive call is. anything has access to f because its curried!
finally, it auto calls create_what_outside_has, and returns the argument which will be the recursive version!
"""

"""
notation prestidigitation
λ f: (λ x: x(x))(λ y: f(λ v: y(y)(v)))
Which is just a Pythonic equivalent of the lambda calculus version:

λf.(λx.x x)(λy.f (λv.((y y) v)))
Essentially you're just doing alternating layers of "call this function" and "recurse this function using autocall". In fact, autocall is itself a combinator, it's called the U combinator. And a combinator, by the way, is just a function that doesn't have any free variables, so it's mostly just jargon.

"""
