import sqlite3
from flask import Flask, jsonify, request, render_template

# Create the Flask app. This is our web server.
app = Flask(__name__)

# SQLite database file. All data is stored here.
DATABASE = "users.db"


def get_db_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Rows become like dicts: row["name"]
    return conn


def row_to_dict(row):
    """Convert one database row to a plain Python dict (for JSON)."""
    return {"id": row["id"], "name": row["name"], "email": row["email"]}


def init_database():
    """Create the users table and add sample records if empty."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
    )
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [
                ("Alice", "alice@example.com"),
                ("Bob", "bob@example.com"),
                ("Charlie", "charlie@example.com"),
            ],
        )
    conn.commit()
    conn.close()


# =============================================================================
# ROUTES (endpoints)
# =============================================================================

# ----- GET /users -----
# HTTP method: GET. Meaning: "Give me all users."
# No request body. Response: JSON array of all users.
@app.route("/users", methods=["GET"])
def get_all_users():
    """Endpoint: GET /users. Returns all users as JSON."""
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    users = [row_to_dict(row) for row in rows]
    # jsonify() converts our list to JSON and sets the right headers.
    return jsonify(users)


# ----- GET /users/<id> -----
# HTTP method: GET. Meaning: "Give me the user with this id."
# The <id> in the URL is a "path parameter". Example: /users/1
@app.route("/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    """Endpoint: GET /users/:id. Returns one user as JSON, or 404 if not found."""
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if row is None:
        # 404 = Not Found. We return JSON with an error message.
        return jsonify({"error": "User not found"}), 404
    return jsonify(row_to_dict(row))


# ----- POST /users -----
# HTTP method: POST. Meaning: "Create a new user."
# The client sends JSON in the request body, e.g. {"name": "Dave", "email": "dave@example.com"}
@app.route("/users", methods=["POST"])
def create_user():
    """Endpoint: POST /users. Creates a new user. Expects JSON body: {name, email}."""
    # request.get_json() reads the request body and parses it as JSON.
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON with 'name' and 'email'"}), 400
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)", (name, email)
    )
    conn.commit()
    new_id = cursor.lastrowid  # ID of the row we just inserted
    conn.close()
    # 201 = Created. We return the new user as JSON.
    return jsonify({"id": new_id, "name": name, "email": email}), 201


# ----- PUT /users/<id> -----
# HTTP method: PUT. Meaning: "Update the user with this id."
# The client sends JSON in the request body, e.g. {"name": "Alice Smith", "email": "alice.smith@example.com"}
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Endpoint: PUT /users/:id. Updates a user. Expects JSON body: {name, email}."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON with 'name' and 'email'"}), 400
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Missing name or email"}), 400
    conn = get_db_connection()
    cursor = conn.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id)
    )
    conn.commit()
    conn.close()
    # rowcount is how many rows were updated. 0 means no user with that id.
    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user_id, "name": name, "email": email})


# ----- DELETE /users/<id> -----
# HTTP method: DELETE. Meaning: "Remove the user with this id."
# No request body. Response: simple success or 404.
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Endpoint: DELETE /users/:id. Deletes a user. No body."""
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"})


# ----- GET / -----
# Serves the HTML page so students can test the API from the browser.
@app.route("/")
def index():
    """Serves the HTML page with forms to test CRUD."""
    return render_template("index.html")


if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
