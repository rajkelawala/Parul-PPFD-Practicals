# Simple RESTful API – Beginner Tutorial

This project is a minimal REST API that uses **SQL** (SQLite) as the database and exposes one endpoint: **GET /users**, which returns a list of users in JSON format.

---

## What You Need

- **Python 3** (3.7 or newer)
- A terminal/command line

SQLite is built into Python, so you don’t need to install a separate database.

---

## Step-by-Step Setup

### 1. Open a terminal and go to this folder

```bash
cd Prac1
```

(Or open the `Prac1` folder in your editor and use its integrated terminal.)

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
```

Activate it:

- **Linux/macOS:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask (the web framework we use for the API).

### 4. Run the server

```bash
python app.py
```

You should see something like:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

The server is now running. Leave this terminal open.

### 5. Test the API and the HTML page

**HTML page (calls the API and shows users):**

- In your browser open: **http://127.0.0.1:5000/**  
- The page uses in-page HTML, CSS, and JavaScript to call `GET /users` and display the list of users.

**Raw API (JSON only):**

- **Browser:** **http://127.0.0.1:5000/users**
- **curl:** `curl http://127.0.0.1:5000/users`
- **Python:** `python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:5000/users').read().decode())"`

---

## Example JSON Response

When you call **GET /users**, the API returns a JSON array of user objects. Example:

```json
[
  {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com"
  },
  {
    "id": 3,
    "name": "Charlie",
    "email": "charlie@example.com"
  }
]
```

Each object has:

- **id** – unique number (from the database)
- **name** – user’s name
- **email** – user’s email

---

## What the Code Does (Summary)

| Step | What happens |
|------|----------------|
| 1 | The app connects to a SQLite database file (`users.db`). |
| 2 | On startup, it creates a `users` table (if it doesn’t exist) with columns: `id`, `name`, `email`. |
| 3 | It inserts three sample users (Alice, Bob, Charlie) if the table is empty. |
| 4 | The route **GET /users** runs a SQL query to fetch all users, converts them to a list of dicts, and returns that list as JSON. |
| 5 | The route **GET /** serves an HTML page (`templates/index.html`) that uses in-page CSS and JavaScript to call the API and show the users. |

All backend logic is in **app.py**; the front end is a single **templates/index.html** with embedded CSS and JS. The goal is clarity for learning, not production-style structure.

---

## Stopping the Server

In the terminal where the server is running, press **Ctrl+C** to stop it.

---

## Troubleshooting

- **“Address already in use”** – Something else is using port 5000. Stop that program or change the port in `app.py` (e.g. `port=5001`).
- **“No module named 'flask'”** – Run `pip install -r requirements.txt` (and make sure your virtual environment is activated if you use one).
- **Empty list `[]`** – Delete the file `users.db` in the `Prac1` folder and restart the server; the table and sample users will be created again.
