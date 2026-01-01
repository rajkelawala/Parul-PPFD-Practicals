# Function to convert a number from any base to decimal
def to_decimal(number, base):
 return int(number, base)

# Function to convert a decimal number to any base
def from_decimal(number, base):
 digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
 result = ""
 while number > 0:
    result = digits[number % base] + result
    number //= base
 return result or "0"


# Input: Number, source base, and target base
number = input("Enter the number: ").strip()
source_base = int(input("Enter the source base (2-36): "))
target_base = int(input("Enter the target base (2-36): "))
# Validate the bases
if not (2 <= source_base <= 36 and 2 <= target_base <= 36):
    print("Bases must be between 2 and 36.")
else:
    try:
        decimal_value = to_decimal(number, source_base)
        converted_number = from_decimal(decimal_value, target_base)
        print(f"The number {number} in base {source_base} is {converted_number} in base {target_base}.")
    except ValueError:
        print("Invalid number for the specified base.")