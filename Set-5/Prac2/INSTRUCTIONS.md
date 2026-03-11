# Prac2: CRUD REST API – Step-by-Step Instructions

This project teaches how **CRUD** (Create, Read, Update, Delete) works in a REST API using **HTTP methods** and **JSON**.

---

## What You Need

- Python 3 (3.7+)
- A terminal and a web browser

---

## Step 1: Install Dependencies

Open a terminal and go to the Prac2 folder:

```bash
cd Prac2
```

Create a virtual environment (recommended):

```bash
python3 -m venv venv
```

Activate it:

- **Linux/macOS:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate`

Install Flask:

```bash
pip install -r requirements.txt
```

---

## Step 2: Run the Server

Start the API server:

```bash
python app.py
```

You should see something like:

```
 * Running on http://127.0.0.1:5001
```

**Leave this terminal open.** The server must keep running while you test.

---

## Step 3: Open the Test Page in Your Browser

In your browser, go to:

**http://127.0.0.1:5001/**

You will see a page with five sections, one for each CRUD operation. Use them to call the API. The response will appear on the page and in the browser console (press **F12** → **Console** tab).

---

## Step 4: Test Each Feature

### 1. Get all users (GET /users)

- On the page: click **Fetch all users**.
- You should see a JSON array of users (e.g. Alice, Bob, Charlie).
- **Or with curl:**  
  `curl http://127.0.0.1:5001/users`

### 2. Get one user (GET /users/:id)

- Enter a user ID (e.g. `1`) and click **Fetch this user**.
- You should see one user object, or `{"error": "User not found"}` if the ID does not exist.
- **Or with curl:**  
  `curl http://127.0.0.1:5001/users/1`

### 3. Create a user (POST /users)

- Enter a **Name** and **Email**, then click **Create user**.
- You should see the new user with an `id` in the response.
- **Or with curl:**  
  `curl -X POST http://127.0.0.1:5001/users -H "Content-Type: application/json" -d '{"name":"Dave","email":"dave@example.com"}'`

### 4. Update a user (PUT /users/:id)

- Enter the user **ID**, **New name**, and **New email**, then click **Update user**.
- You should see the updated user object.
- **Or with curl:**  
  `curl -X PUT http://127.0.0.1:5001/users/1 -H "Content-Type: application/json" -d '{"name":"Alice Smith","email":"alice.smith@example.com"}'`

### 5. Delete a user (DELETE /users/:id)

- Enter the user **ID** and click **Delete user**.
- You should see `{"message": "User deleted"}`.
- **Or with curl:**  
  `curl -X DELETE http://127.0.0.1:5001/users/3`

---

## Example API Request and Response Samples

### GET /users (get all users)

**Request:**

- Method: `GET`
- URL: `http://127.0.0.1:5001/users`
- Body: none

**Response (200 OK):**

```json
[
  { "id": 1, "name": "Alice", "email": "alice@example.com" },
  { "id": 2, "name": "Bob", "email": "bob@example.com" },
  { "id": 3, "name": "Charlie", "email": "charlie@example.com" }
]
```

---

### GET /users/1 (get one user)

**Request:**

- Method: `GET`
- URL: `http://127.0.0.1:5001/users/1`
- Body: none

**Response (200 OK):**

```json
{ "id": 1, "name": "Alice", "email": "alice@example.com" }
```

**Response if not found (404):**

```json
{ "error": "User not found" }
```

---

### POST /users (create user)

**Request:**

- Method: `POST`
- URL: `http://127.0.0.1:5001/users`
- Headers: `Content-Type: application/json`
- Body: `{"name": "Dave", "email": "dave@example.com"}`

**Response (201 Created):**

```json
{ "id": 4, "name": "Dave", "email": "dave@example.com" }
```

**Response if body is invalid (400):**

```json
{ "error": "Missing name or email" }
```

---

### PUT /users/1 (update user)

**Request:**

- Method: `PUT`
- URL: `http://127.0.0.1:5001/users/1`
- Headers: `Content-Type: application/json`
- Body: `{"name": "Alice Smith", "email": "alice.smith@example.com"}`

**Response (200 OK):**

```json
{ "id": 1, "name": "Alice Smith", "email": "alice.smith@example.com" }
```

**Response if user not found (404):**

```json
{ "error": "User not found" }
```

---

### DELETE /users/3 (delete user)

**Request:**

- Method: `DELETE`
- URL: `http://127.0.0.1:5001/users/3`
- Body: none

**Response (200 OK):**

```json
{ "message": "User deleted" }
```

**Response if user not found (404):**

```json
{ "error": "User not found" }
```

---

## Quick Reference

| Action   | HTTP method | Endpoint      | Body (JSON)        |
|----------|-------------|---------------|--------------------|
| Get all  | GET         | /users        | —                  |
| Get one  | GET         | /users/:id    | —                  |
| Create   | POST        | /users        | { name, email }    |
| Update   | PUT         | /users/:id    | { name, email }    |
| Delete   | DELETE      | /users/:id    | —                  |

---

## Stopping the Server

In the terminal where the server is running, press **Ctrl+C**.

---

## Files in This Project

- **app.py** – Backend: all CRUD endpoints and database code (with comments).
- **templates/index.html** – Frontend: forms and buttons that call the API with `fetch()` (with comments).
- **requirements.txt** – Python dependencies (Flask).
- **users.db** – SQLite database (created when you first run the server).

The goal of this project is **clarity for learning**, not production-style code.
