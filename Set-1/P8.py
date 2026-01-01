numbers = input("Enter a list of numbers separated by spaces: ")
numbers = [int(num) for num in numbers.split()]

print("Choose sorting order:")
print("1. Ascending")
print("2. Descending")

choice = input("Enter your choice (1 or 2): ")

if choice == "1":
    numbers.sort()
    print("Numbers sorted in ascending order:", numbers)
elif choice == "2":
    numbers.sort(reverse=True)
    print("Numbers sorted in descending order:", numbers)
else:
    print("Invalid choice. Please enter 1 or 2.")