# variables are used to store data that can be referenced and manipulated during running of a program


# python variables do not require declaration of type
# i.e. we dont explicitly mention whether its a string, integer or boolean value etc.

x = 5 # x is integer here
print(x)

x = "Python" # x is string here (automatically understood by python)

# see how we changed the varible value from 5 to "Python"

print(x)

# ------------------

country = "India"
print(country)

country = "Japan"
print(country)

# but there are rules for variables


# concept of object reference

a = 10
b = a
print(a) # 10
print(b) # 10

a = 20
print(a) # 20
print(b) # 10

b = 30
print(a) # 20
print(b) # 10


