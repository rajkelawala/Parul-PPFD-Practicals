import csv

file_name = input("Enter the CSV file name: ")
column_name = input("Enter the column name to calculate the average: ")
try:
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        total = 0
        count = 0
        for row in csv_reader:
            try:
                total += float(row[column_name])
                count += 1
            except ValueError:
                print(f"Skipping invalid data: {row[column_name]}")
            except KeyError:
                print(f"Column '{column_name}' not found in the file.")
                break
        if count > 0:
            average = total / count
            print(f"The average of the '{column_name}' column is: {average}")
        else:
            print(f"No valid data found in column '{column_name}'.")
except FileNotFoundError:
    print(f"The file '{file_name}' was not found. Please check the file name and try again.")