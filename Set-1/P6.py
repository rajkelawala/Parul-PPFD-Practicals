num = int(input("Enter a number: "))

factorial = 1

for i in range(1, num + 1):
    factorial *= i   # factorial = factorial * i

print("Factorial of", num, "is:", factorial)

#5*4*3*2*1
