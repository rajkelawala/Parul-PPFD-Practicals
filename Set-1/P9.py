number = int(input("Enter a number to generate its multiplication table: "))

upto = int(input("Enter the range (e.g., 10 for 1 to 10): "))
print(f"\nMultiplication Table for {number}:")

for i in range(1, upto + 1):
    print(f"{number} x {i} = {number * i}")

#range(1,5)