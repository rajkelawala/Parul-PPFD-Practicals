from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
# Database file
DATABASE = "data.db"

# Function to initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create a sample table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        salary REAL NOT NULL
        )
        """)
    # Insert sample data if the table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        sample_data = [
        ("Alice", "Software Engineer", 75000),
        ("Bob", "Data Analyst", 65000),
        ("Charlie", "Project Manager", 85000),
        ]
        cursor.executemany("INSERT INTO employees (name, position, salary)VALUES (?, ?, ?)", sample_data)
    conn.commit()
# Route to display data in a tabular format
@app.route("/")
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall() # Fetch all rows from the table
    return render_template("table.html", employees=employees)
# Run the app
if __name__ == "__main__":
    init_db() # Initialize the database
    app.run(debug=True)