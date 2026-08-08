# functions
# reusbale blocks of code


# syntax

# use def keyword
def my_func(): # function name has rules same as variables
  pass # pass keyword. just nothing happens

# why functions? reusability

# many aspects of functions

def func1():

  return # returns some value or nothing
  # a return statement terminates the function execution immediately

# return multiple values as tuple

def func2():
  print("We are inside the function now.")
  return "Hello", "Earth"


result = func2()
print(result)

def func3(a, b, c): # arguments
  return a+b+c


sum_of_numbers = func3(1,2,3) # parameters


# take x,y,z as user input and pass them
# sum_of_numbers = func3(x,y,z)


# pass by reference vs pass by value

# lists = mutable
# int, str = immutable

def func4(L):
  L[1] = 100

sample_list = [1,2,3,4,5]
func4(sample_list)
print(sample_list)

def func5(x):
  x = 500

x = 10
func5(x)
print(x)
