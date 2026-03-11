# Prac5: Data Validation and Error Handling – Step-by-Step Guide

This project teaches **why validation is necessary**, **how errors are returned**, and **how the frontend shows success and failure**.

---

## What You Need

- Python 3 (3.7+)
- A terminal and a web browser

---

## Step 1: Install and Run

```bash
cd Prac5
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server runs at **http://127.0.0.1:5004**. Leave the terminal open.

---

## Step 2: Open the Test Page

Go to **http://127.0.0.1:5004/** and open the browser console (F12 → Console). You will see every request and response logged.

---

## Step 3: Demonstrate Success and Failure

### Successful request

1. **Create user:** Fill Name (e.g. Dave), Email (dave@example.com), Age (25). Click **Create user**.
2. You should see **HTTP 201** and the new user in the **Success** box (green).
3. In the console you will see the full JSON response with `success: true` and `data`.

### Empty form (validation error)

1. Leave Name, Email, and Age empty. Click **Create user**.
2. You should see **HTTP 400** and a message like "Name is required and cannot be empty" (or similar) in the **Error** box (red).
3. Console shows `success: false`, `error`, `details`.

### Invalid email

1. Enter Name: Test, Email: `notanemail`, Age: 20. Click **Create user**.
2. **HTTP 400** – "Email must be a valid format (e.g. user@example.com)."

### Age &lt; 18

1. Enter Name: Young, Email: young@example.com, Age: 17. Click **Create user**.
2. **HTTP 400** – "Age must be 18 or older."

### Duplicate email

1. Create a user with email `alice@example.com` (or use the sample user’s email). Click **Create user**.
2. **HTTP 400** – "Email is already in use."

### Non-existent user (404)

1. **Get one / Update / Delete:** Use User ID **999** (or any ID that does not exist). Click **Update user** or **Delete user**.
2. **HTTP 404** – "User not found." (or similar). Error box shows the message.

After each case, check the console for the full response body and status code.

---

## Flow Diagram (Text)

```
  CLIENT (browser)                    SERVER (Flask)

  1. Send data (e.g. POST /users with name, email, age)
     ----------------------------------------------->
                                              Parse JSON (if invalid → 400)
                                              Validate: name, email, age
                                              If invalid → 400 + { success: false, error, details }
     If Invalid:
     2. Response 400 + JSON error
        <-----------------------------------------------
        UI shows error in red, logs in console

     If Valid:
                                              Insert into DB (if duplicate email → 400)
     2. Response 200/201 + { success: true, data }
        <-----------------------------------------------
        UI shows success in green, logs in console
```

So: **Client sends data → Server validates → If invalid, return 400 and structured error → UI shows error. If valid, save and return 200/201 and data → UI shows success.**

---

## Example: Valid Request and Response

**Request:** POST /users

- Headers: `Content-Type: application/json`
- Body: `{"name": "Dave", "email": "dave@example.com", "age": 25}`

**Response (201 Created):**

```json
{
  "success": true,
  "data": {
    "id": 4,
    "name": "Dave",
    "email": "dave@example.com",
    "age": 25
  }
}
```

---

## Example: Invalid Request and Response

**Request:** POST /users

- Body: `{"name": "", "email": "bad", "age": 17}`

**Response (400 Bad Request):**

```json
{
  "success": false,
  "error": "Validation Error",
  "details": "Name is required and cannot be empty."
}
```

(The server returns one error at a time; the first validation failure is returned. You might get "Age must be 18 or older." if name and email were valid.)

---

## Why Validation and Error Handling Matter

- **Without validation:** Bad data (empty name, invalid email, age 5) can be stored. The database might get duplicate emails or invalid values, and the app becomes inconsistent.
- **Without error handling:** Invalid JSON or a database error could crash the server. With try/except we return 400 or 500 and a clear message, so the API stays stable and the client knows what went wrong.
- **Structured errors:** Always returning `{ success, error, details }` for failures lets the frontend show one consistent “details” message and use the status code to decide style (e.g. red for error, green for success).

---

## Files in This Project

- **app.py** – CRUD for users (id, name, email, age). Validation for name, email, age (required; age ≥ 18; email format and uniqueness). Structured 400/404/500 responses. Centralized try/except for invalid JSON, missing body, and database errors. Comments explain validation, status codes, and edge cases.
- **templates/index.html** – Create form, update form, fetch all, delete. Error box (red) and success box (green), HTTP status shown, console logging. Comments explain how the frontend reads status and parses JSON and why backend validation is still required.
- **requirements.txt** – Flask.
- **users.db** – SQLite (created on first run). Sample users: Alice, Bob, Charlie (all age ≥ 18).

The goal is **conceptual clarity**: what validation is, why it matters, how errors propagate, and how the frontend handles backend errors.
