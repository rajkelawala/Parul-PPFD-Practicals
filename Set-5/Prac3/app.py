

import sqlite3
import time
from flask import Flask, jsonify, request, render_template
import jwt

# Create the Flask app.
app = Flask(__name__)

# Database file.
DATABASE = "users.db"

# Secret key used to sign and verify JWTs.
# In production we would use an environment variable and a long random string.
# Anyone with this key can create valid tokens, so keep it secret on the server.
SECRET_KEY = "my-secret-key-for-learning-only"

# How long the token is valid (in seconds). 1 hour = 3600.
TOKEN_EXPIRY_SECONDS = 3600


def get_db_connection():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Create the users table and insert one sample user.
    We store password in PLAIN TEXT only for teaching. In production we must use
    hashing (e.g. bcrypt) - never store plain text passwords.
    """
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Sample user: email alice@example.com, password "password123"
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ("Alice", "alice@example.com", "password123"),
        )
    conn.commit()
    conn.close()


# ----- Helper: create a JWT for a user -----
# JWT has three parts: HEADER.PAYLOAD.SIGNATURE
# - Header: type of token and algorithm (e.g. HS256).
# - Payload: our data (user_id, email) plus standard claim "exp" (expiration time).
# - Signature: server signs header+payload with SECRET_KEY so we can verify later that nothing was changed.
def create_token(user_id, email):
    """
    Create a JWT containing user_id and email. The library adds 'exp' (expiration) for us.
    Token creation step by step (inside jwt.encode):
      1. Build header (e.g. {"alg": "HS256", "typ": "JWT"}).
      2. Build payload with our data + exp time.
      3. Sign header + payload with SECRET_KEY to produce the signature.
      4. Return "header.payload.signature" as a string.
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": int(time.time()) + TOKEN_EXPIRY_SECONDS,  # Expiration time (Unix timestamp).
    }
    # jwt.encode(payload, secret, algorithm) returns the full JWT string.
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # In PyJWT 2+, encode returns a string; in older versions it might be bytes.
    if hasattr(token, "decode"):
        token = token.decode("utf-8")
    return token


# ----- Helper: verify a JWT and return the payload -----
def verify_token(token_string):
    """
    Verify the JWT and return the payload (dict with user_id, email, etc.).
    Token verification step by step (inside jwt.decode):
      1. Split the token into header, payload, signature.
      2. Recompute the signature using header + payload + SECRET_KEY.
      3. If it matches the signature in the token, the token was not tampered with.
      4. Check that "exp" (expiration) has not passed.
      5. Return the payload. If anything is wrong, jwt.decode raises an exception.
    """
    try:
        payload = jwt.decode(token_string, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired.
    except jwt.InvalidTokenError:
        return None  # Token invalid (wrong signature, bad format, etc.).


# =============================================================================
# ROUTES
# =============================================================================

# ----- POST /register (public) -----
# Create a new user. No token required.
@app.route("/register", methods=["POST"])
def register():
    """
    Create a new user. Expects JSON: { "name", "email", "password" }.
    We store password in plain text for simplicity - NOT for production use.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON with name, email, password"}), 400
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    if not name or not email or not password:
        return jsonify({"error": "Missing name, email, or password"}), 400
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password),
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        conn.rollback()
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()


# ----- POST /login (public) -----
# Validate email and password, then return a JWT.
@app.route("/login", methods=["POST"])
def login():
    """
    Check email and password. If correct, create a JWT and return it.
    The client will send this token in the Authorization header for protected routes.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON with email and password"}), 400
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, name, email FROM users WHERE email = ? AND password = ?",
        (email, password),
    ).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Invalid email or password"}), 401
    # Create JWT with user id and email in the payload.
    token = create_token(user_id=row["id"], email=row["email"])
    return jsonify({"token": token, "message": "Login successful"})


# ----- GET /profile (protected) -----
# Requires a valid JWT in the Authorization header.
@app.route("/profile", methods=["GET"])
def profile():
    """
    Protected route: only works if the client sends a valid JWT.
    We read the token from the "Authorization" header. Convention: "Bearer <token>".
    If token is missing or invalid, we return an error.
    """
    # The client sends: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token missing. Send header: Authorization: Bearer <token>"}), 401
    token_string = auth_header[7:]  # Remove "Bearer " to get the token.
    payload = verify_token(token_string)
    if payload is None:
        return jsonify({"error": "Token invalid or expired"}), 401
    # Token is valid. We have user_id and email in the payload. Fetch fresh data from DB.
    user_id = payload["user_id"]
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, name, email FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
    })


# ----- GET / -----
# Serve the HTML page for testing.
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)
