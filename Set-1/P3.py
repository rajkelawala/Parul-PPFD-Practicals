import random
import string

# Ask user for password length
length = int(input("Enter password length: "))

# Characters to use in password
characters = string.ascii_letters + string.digits + string.punctuation

# Generate password
password = ''.join(random.choice(characters) for i in range(length))
print("Your generated password is:", password)