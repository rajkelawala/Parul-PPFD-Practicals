# Display menu for the user
print("Temperature Conversion Program")
print("1. Convert Fahrenheit to Celsius")
print("2. Convert Celsius to Fahrenheit")

# Get user's choice
choice = input("Enter your choice (1 or 2): ")#1
if choice == "1":
    fahrenheit = float(input("Enter temperature in Fahrenheit: "))
    celsius = (fahrenheit - 32) * 5 / 9
    print(f"{fahrenheit}°F is equal to {celsius:.2f}°C")
elif choice == "2":
 # Celsius to Fahrenheit conversion
    celsius = float(input("Enter temperature in Celsius: "))
    fahrenheit = (celsius * 9 / 5) + 32
    print(f"{celsius}°C is equal to {fahrenheit:.2f}°F")
else:
 # Handle invalid input
    print("Invalid choice. Please enter 1 or 2.")

 #kuasbvlas
 #kabsckjbas
