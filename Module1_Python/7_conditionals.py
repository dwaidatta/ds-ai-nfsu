# conditionals
# statements to control flow of the program

# if

age = 20
if age >= 18:
  print("Eligible to vote.")


# if else

age = 20
if age >= 18:
  print("Eligible to vote.")
else:
  print("Not eligible.")


# if elif else
# else can be missing too

age = 25

if age <= 12:
  print("Child.")
elif age <= 19:
  print("Teenager.")
elif age <= 35:
  print("Young adult.")
else:
  print("Adult.")


# nested if else


# conditional ternary

print("Adult" if age >= 18 else "Small")


# match case statement
# not commonly used