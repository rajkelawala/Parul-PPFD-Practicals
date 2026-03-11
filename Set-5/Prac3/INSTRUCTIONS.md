# Prac3: JWT Authentication – Step-by-Step Guide

This project teaches how **authentication** works using **JSON Web Tokens (JWT)**. You will register a user, log in to get a token, and use that token to access a protected route.

---

## What You Need

- Python 3 (3.7+)
- A terminal and a web browser

---

## Step 1: Install Dependencies

Open a terminal and go to the Prac3 folder:

```bash
cd Prac3
```

Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

This installs **Flask** (web framework) and **PyJWT** (create and verify JWTs).

---

## Step 2: Run the Server

Start the API:

```bash
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5002
```

Leave this terminal open.

---

## Step 3: Open the Test Page in Your Browser

Go to:

**http://127.0.0.1:5002/**

Open the browser console (F12 → Console tab) so you can see logs for every API call.

---

## Step 4: Register a New User

1. In the **Register** section, enter:
   - Name: e.g. Bob  
   - Email: e.g. bob@example.com  
   - Password: e.g. secret123  
2. Click **Register**.
3. You should see: `"message": "User registered successfully"` (HTTP 201).
4. In the console you will see the request and response.

---

## Step 5: Login to Get a JWT

1. In the **Login** section, use either:
   - **Sample user:** email `alice@example.com`, password `password123`  
   - Or the user you just registered.
2. Click **Login**.
3. The response will include a **token** (a long string). The page automatically saves it in **localStorage** and shows it in the "Current token" box.
4. In the console you will see that the token was saved.

**What just happened:** The server checked your email and password, then created a JWT containing your user id and email, signed with the secret key. That string is your "ticket" for protected routes.

---

## Step 6: Access the Protected Route (With Token)

1. Make sure you are logged in (token box shows a long string).
2. Click **Get my profile**.
3. You should see your user data: `id`, `name`, `email` (HTTP 200).
4. In the console you will see that the request was sent with the header `Authorization: Bearer <token>`.

**What just happened:** The browser read the token from localStorage and sent it in the **Authorization** header. The server verified the JWT and returned your profile.

---

## Step 7: Test With Invalid or Missing Token

**Token missing:**

1. Click **Clear token**.
2. Click **Get my profile** again.
3. You should see: `"error": "Token missing. Send header: Authorization: Bearer <token>"` (HTTP 401).

**Token invalid:**

1. In the token box, you could manually change a character in the token (or type "invalid").
2. Click **Get my profile**.
3. You should see: `"error": "Token invalid or expired"` (HTTP 401).

This shows that the server **authorizes** the request only when the token is valid.

---

## JWT Flow – Simple Diagram (Text)

```
  CLIENT (browser)                    SERVER (Flask)

  1. POST /login
     Body: { email, password }
     ----------------------------------------------->
                                              Check email & password in DB
                                              Create JWT (header.payload.signature)
     2. Response: { token: "eyJ..." }
     <-----------------------------------------------
     Save token in localStorage

  3. GET /profile
     Header: Authorization: Bearer eyJ...
     ----------------------------------------------->
                                              Read "Authorization" header
                                              Verify JWT signature with secret key
                                              If valid, get user_id from payload
                                              Return user data from DB
     4. Response: { id, name, email }
     <-----------------------------------------------
     Show profile on page
```

- **Login:** Client proves identity with password → Server returns a **token**.
- **Protected route:** Client sends the **token** in the **Authorization** header → Server verifies it and sends back data.

---

## Example Request and Response Samples

### POST /register (create user)

**Request:**

- URL: `http://127.0.0.1:5002/register`
- Method: `POST`
- Headers: `Content-Type: application/json`
- Body: `{"name": "Bob", "email": "bob@example.com", "password": "secret123"}`

**Response (201 Created):**

```json
{
  "message": "User registered successfully"
}
```

**Response if email exists (400):**

```json
{
  "error": "Email already exists"
}
```

---

### POST /login (get JWT)

**Request:**

- URL: `http://127.0.0.1:5002/login`
- Method: `POST`
- Headers: `Content-Type: application/json`
- Body: `{"email": "alice@example.com", "password": "password123"}`

**Response (200 OK):**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6ImFsaWNlQGV4YW1wbGUuY29tIiwiZXhwIjoxNzE5...",
  "message": "Login successful"
}
```

**Response if wrong password (401):**

```json
{
  "error": "Invalid email or password"
}
```

---

### GET /profile (protected – with token)

**Request:**

- URL: `http://127.0.0.1:5002/profile`
- Method: `GET`
- Headers: `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (the token from login)

**Response (200 OK):**

```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

**Response if token missing (401):**

```json
{
  "error": "Token missing. Send header: Authorization: Bearer <token>"
}
```

**Response if token invalid or expired (401):**

```json
{
  "error": "Token invalid or expired"
}
```

---

## Quick Reference

| Route           | Method | Auth required? | Purpose              |
|----------------|--------|----------------|----------------------|
| /register      | POST   | No             | Create new user      |
| /login         | POST   | No             | Get JWT              |
| /profile       | GET    | Yes (JWT)      | Get current user     |

- **Authentication** = proving who you are (login with email/password).
- **Authorization** = being allowed to do something (e.g. only with valid JWT for /profile).
- **JWT** = token string (header.payload.signature); server signs it with a **secret key** and verifies it on each protected request.

---

## Files in This Project

- **app.py** – Backend: register, login, JWT create/verify, protected /profile. Heavily commented.
- **templates/index.html** – Frontend: register form, login form, token display, “Get my profile” button. Uses `fetch()`, localStorage, and Authorization header. Heavily commented.
- **requirements.txt** – Flask and PyJWT.
- **users.db** – SQLite database (created on first run). Passwords are stored in **plain text for teaching only**; in production we would use hashing (e.g. bcrypt).

The goal is **conceptual clarity** and hands-on learning, not production-grade security.
