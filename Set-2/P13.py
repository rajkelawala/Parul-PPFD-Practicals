file_name = input("Enter the file name: ")
try:
    with open(file_name, 'r') as file:
        content = file.read()
        words = content.split()
        word_count = len(words)
        print(f"The file '{file_name}' contains {word_count} words.")
except FileNotFoundError:
    print(f"The file '{file_name}' was not found. Please check the file name and try again.")
