import sqlite3
from flask import Flask, jsonify, render_template

# Create the Flask app. This is our "web server" that will respond to requests.
app = Flask(__name__)

# The path to our database file. SQLite stores everything in this one file.
DATABASE = "users.db"


def get_db_connection():

    # connect() opens the file. If it doesn't exist, SQLite creates it.
    conn = sqlite3.connect(DATABASE)
    # This makes rows behave like dictionaries (we can use column names).
    conn.row_factory = sqlite3.Row
    return conn


def init_database():

    conn = get_db_connection()

    # Create the users table if it doesn't exist.
    # id: unique number for each user (auto-increment)
    # name and email: text fields
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
    )

    # Check if we already have users (so we don't insert duplicates on every restart).
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert a few sample users. Each tuple is one row: (name, email).
        conn.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [
                ("Alice", "alice@example.com"),
                ("Bob", "bob@example.com"),
                ("Charlie", "charlie@example.com"),
            ],
        )

    # Save changes and close the connection.
    conn.commit()
    conn.close()


# Serve the HTML page that calls the API (same app, so no CORS issues).
@app.route("/")
def index():
    return render_template("index.html")


# API endpoint: GET /users
# When someone visits http://localhost:5000/users (with GET), this function runs.
@app.route("/users", methods=["GET"])
def get_users():
    """
    Fetches all users from the database and returns them as JSON.
    """
    # Open a connection to the database.
    conn = get_db_connection()

    # Run a SQL query: select all columns from the users table.
    rows = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()

    # Convert each row to a plain Python dict (id, name, email).
    # sqlite3.Row objects are converted so they can be serialized to JSON.
    users = [{"id": row["id"], "name": row["name"], "email": row["email"]} for row in rows]

    # jsonify() turns our list of dicts into a proper JSON response with
    # the right headers (Content-Type: application/json).
    return jsonify(users)


# This block runs only when we execute this file directly (python app.py).
# It does NOT run when the file is imported.
if __name__ == "__main__":
    # First, create the table and insert sample users.
    init_database()
    # Start the development server. Visit http://127.0.0.1:5000
    # debug=True makes the server reload when we change the code (handy for learning).
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
