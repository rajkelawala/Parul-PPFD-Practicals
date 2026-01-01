# Taking numbers from user
numbers = input("Enter numbers separated by space: ").split()

# Convert all inputs (strings) into integers
numbers = [int(num) for num in numbers]
# Calculate total and average
total = sum(numbers)
count = len(numbers)
average = total / count

print("Average is:", average)
#[1,2,3,4,5,76,7]+