year = int(input("Enter a year: "))

# Leap year conditions:
# 1. Year divisible by 4
# 2. But not divisible by 100
# 3. Unless also divisible by 400

if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
    print(year, "is a leap year")
else:
    print(year, "is not a leap year")