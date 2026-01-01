import pandas as pd

file_name = input("Enter the Excel file name (with .xlsx or .xls extension): ")
try:
    data = pd.read_excel(file_name, engine='openpyxl')
    print("\nData in the Excel file:")
    print(data.to_markdown(index=False))
except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found. Please check the file path.")
except PermissionError:
        print(f"Error: Permission denied. Close the file if it's open in another application.")
except ValueError as e:
        print(f"Error: {e}. Ensure the file is in a valid Excel format (.xlsx or .xls).")
except Exception as e:
    print(f"An unexpected error occurred: {e}")