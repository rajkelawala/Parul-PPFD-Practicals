"""
Prac5: Data Validation and Error Handling in REST APIs
==========================================================================

What is VALIDATION?
  Validation means checking that the data we receive (e.g. from a form or API request)
  meets our rules before we use it. Examples: "name must not be empty", "age must be 18 or older".
  Without validation, bad input can break the app or the database.

What is SERVER-SIDE VALIDATION?
  The server (this Python code) checks every request. Even if the frontend sends invalid
  data – or someone calls the API directly with a tool like curl – we still enforce the rules.
  We never trust the client. Server-side validation is required for security and data integrity.

What is CLIENT-SIDE VALIDATION?
  The browser (JavaScript) can check the form before sending: "Is email empty? Is age a number?"
  This gives quick feedback to the user. But it is not enough: users can disable JavaScript,
  or send requests without using our form. So we always validate on the server too.

What is ERROR HANDLING?
  When something goes wrong (invalid input, missing resource, database error), we don't let
  the program crash. We catch the error and return a clear response to the client. That way
  the API stays stable and the client knows what went wrong.

What is an HTTP STATUS CODE?
  A number the server sends with every response. The client uses it to know the result.
  - 200 OK         = Request succeeded.
  - 201 Created    = Resource was created (e.g. POST /users).
  - 400 Bad Request = Client sent invalid data (validation failed). Client should fix the request.
  - 404 Not Found  = The requested resource (e.g. user id 999) does not exist.
  - 500 Internal Server Error = Something went wrong on the server (bug, database down). Not the client's fault.

Why different status codes matter:
  The frontend can show different messages: 400 → "Please fix the form." 404 → "User not found."
  500 → "Something went wrong on our side." Without proper codes, the client cannot react correctly.

Why validation is necessary / why trusting user input is dangerous:
  - Users can send empty names, invalid emails, or age = -5. If we don't check, we might insert
    bad data and break database integrity (e.g. duplicate emails, negative ages).
  - Malicious users can send huge strings or wrong types to crash the server. Validation and
    error handling protect the system.

Why structured error responses improve API design:
  We return the same shape for errors: { "success": false, "error": "...", "details": "..." }.
  The frontend can always read "success" and "details" and show a consistent message. Chaos
  happens when every endpoint returns errors in a different format.
"""

import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
DATABASE = "users.db"

# Maximum length for name and email to avoid extremely long input (edge case).
# Without this, someone could send a 1MB string and cause memory or display issues.
MAX_NAME_LENGTH = 200
MAX_EMAIL_LENGTH = 254


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    return {"id": row["id"], "name": row["name"], "email": row["email"], "age": row["age"]}


def error_response(message, details, status_code=400):
    """Return a structured error JSON. Same shape for all errors so the frontend can parse consistently."""
    return jsonify({
        "success": False,
        "error": message,
        "details": details,
    }), status_code


def success_response(data, status_code=200):
    """Return a structured success JSON."""
    return jsonify({"success": True, "data": data}), status_code


def validate_email(email):
    """
    Simple email format check: must contain @ and at least one dot after @.
    Not as strict as a full RFC validator, but enough for teaching.
    """
    if not email or not isinstance(email, str):
        return False
    email = email.strip()
    if len(email) > MAX_EMAIL_LENGTH:
        return False
    return "@" in email and "." in email.split("@")[-1]


def validate_user_data(data, for_update=False, existing_user_id=None):
    """
    Validate name, email, age for create or update.
    Returns (None, None) if valid, or (status_code, error_response) if invalid.
    """
    if not data or not isinstance(data, dict):
        return 400, error_response(
            "Bad Request",
            "Request body must be JSON with name, email, and age.",
            400,
        )

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    # name: required, not empty
    if name is None or (isinstance(name, str) and not name.strip()):
        return 400, error_response("Validation Error", "Name is required and cannot be empty.", 400)
    name = str(name).strip()
    if len(name) > MAX_NAME_LENGTH:
        return 400, error_response("Validation Error", "Name is too long.", 400)

    # email: required, valid format
    if email is None or (isinstance(email, str) and not email.strip()):
        return 400, error_response("Validation Error", "Email is required and cannot be empty.", 400)
    email = str(email).strip().lower()
    if len(email) > MAX_EMAIL_LENGTH:
        return 400, error_response("Validation Error", "Email is too long.", 400)
    if not validate_email(email):
        return 400, error_response("Validation Error", "Email must be a valid format (e.g. user@example.com).", 400)

    # age: required, number, >= 18
    if age is None:
        return 400, error_response("Validation Error", "Age is required.", 400)
    try:
        age_int = int(age) if isinstance(age, (int, float)) else int(float(age))
    except (ValueError, TypeError):
        return 400, error_response("Validation Error", "Age must be a number.", 400)
    if age_int < 18:
        return 400, error_response("Validation Error", "Age must be 18 or older.", 400)

    # Check email uniqueness: for POST, email must not exist; for PUT, must not exist for another user
    conn = get_db_connection()
    if for_update and existing_user_id is not None:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ? AND id != ?", (email, existing_user_id)
        ).fetchone()
    else:
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if existing:
        return 400, error_response("Validation Error", "Email is already in use.", 400)

    return None, {"name": name, "email": email, "age": age_int}


def init_database():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER NOT NULL CHECK (age >= 18)
        )
        """
    )
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            [
                ("Alice", "alice@example.com", 25),
                ("Bob", "bob@example.com", 30),
                ("Charlie", "charlie@example.com", 22),
            ],
        )
    conn.commit()
    conn.close()


# =============================================================================
# ROUTES – with centralized error handling
# =============================================================================
# Why try/except? If we don't catch errors, one bad request (e.g. invalid JSON, DB error)
# can crash the whole server. By catching we return a 400 or 500 and keep the server running.
# What happens if errors are not handled? Unhandled exceptions terminate the request and
# often return a generic 500 or an HTML error page, and the client gets no structured message.


@app.route("/users", methods=["GET"])
def get_all_users():
    try:
        conn = get_db_connection()
        rows = conn.execute("SELECT id, name, email, age FROM users").fetchall()
        conn.close()
        users = [row_to_dict(row) for row in rows]
        return success_response(users)
    except Exception as e:
        return error_response("Internal Server Error", str(e), 500)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_one_user(user_id):
    try:
        conn = get_db_connection()
        row = conn.execute(
            "SELECT id, name, email, age FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return error_response("Not Found", "User not found.", 404)
        return success_response(row_to_dict(row))
    except Exception as e:
        return error_response("Internal Server Error", str(e), 500)


@app.route("/users", methods=["POST"])
def create_user():
    # Edge case: missing JSON body or wrong Content-Type. get_json() returns None if body is not JSON.
    try:
        data = request.get_json(force=False, silent=False)
    except Exception:
        return error_response(
            "Bad Request",
            "Request body must be valid JSON with Content-Type: application/json.",
            400,
        )
    if data is None:
        return error_response(
            "Bad Request",
            "Request body must be JSON with name, email, and age.",
            400,
        )

    err_code, err_resp = validate_user_data(data, for_update=False)
    if err_code is not None:
        return err_resp
    valid = err_resp  # validated dict: name, email, age
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (valid["name"], valid["email"], valid["age"]),
        )
        conn.commit()
        new_id = cursor.lastrowid
        row = conn.execute("SELECT id, name, email, age FROM users WHERE id = ?", (new_id,)).fetchone()
        conn.close()
        return success_response(row_to_dict(row), 201)
    except sqlite3.IntegrityError as e:
        # SQL constraint violations: e.g. unique email violated if two requests race.
        return error_response("Validation Error", "Email may already be in use or constraint violated.", 400)
    except Exception as e:
        return error_response("Internal Server Error", str(e), 500)


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json(force=False, silent=False)
    except Exception:
        return error_response(
            "Bad Request",
            "Request body must be valid JSON with Content-Type: application/json.",
            400,
        )
    if data is None:
        return error_response(
            "Bad Request",
            "Request body must be JSON with name, email, and age.",
            400,
        )

    err_code, err_resp = validate_user_data(data, for_update=True, existing_user_id=user_id)
    if err_code is not None:
        return err_resp
    valid = err_resp
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
            (valid["name"], valid["email"], valid["age"], user_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return error_response("Not Found", "User not found.", 404)
        row = conn.execute("SELECT id, name, email, age FROM users WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        return success_response(row_to_dict(row))
    except sqlite3.IntegrityError:
        return error_response("Validation Error", "Email may already be in use.", 400)
    except Exception as e:
        return error_response("Internal Server Error", str(e), 500)


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return error_response("Not Found", "User not found.", 404)
        return success_response({"message": "User deleted"})
    except Exception as e:
        return error_response("Internal Server Error", str(e), 500)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5004, debug=True, use_reloader=False)
