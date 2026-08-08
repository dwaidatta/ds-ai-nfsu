# operators: does action on operand(s)
# operand: gets acted on by operator(s)

# arithmetic operator
# basic math
# + - / // * %

print(5 + 11)
print(11 / 5)
print(11 // 5) # floor division or integer division
print(11 * 5)
print(11 % 5)

# relational operators
# find relation among two operands
# > < == != etc

# returns boolean value True False

print(10 > 5) # True
print(10 != 5) # True
print(10 <= 5) # False


# logical operators
# do logical operations based on logical gates
# combines relational statements
# and or not

print(not True) #False
print(True and False)
print(True or False)
print(not False and True)


# bitwise operators
# works on bits
# not done



# assignment operators
# assigns values
# right side value assigned to left side operand
# = += -= *= etc
# some are shorthand operators

a = 5
a += 10 # a = a + 10 => a = 5 + 10

# identity operators
# check values if they are located on same part of memory

a = 10
b = 10
c = a

print(a is not b) # False
print(a is c) # True


# membership operators
# present in sequence?
# in not in




# ternary operators

min_value = 5 if 5 < 10 else 10
print(min_value)


