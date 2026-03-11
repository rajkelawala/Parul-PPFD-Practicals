# Prac4: Pagination in REST APIs – Step-by-Step Guide

This project teaches **pagination**: how to return large lists in small chunks (pages) and why that improves performance.

---

## What You Need

- Python 3 (3.7+)
- A terminal and a web browser

---

## Step 1: Install Dependencies

```bash
cd Prac4
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Step 2: Run the Server

```bash
python app.py
```

You should see: `Running on http://127.0.0.1:5003`. Leave the terminal open.

---

## Step 3: Open the Test Page

In your browser go to: **http://127.0.0.1:5003/**

Open the console (F12 → Console) to see the URL and response for each request.

---

## Step 4: Use the UI

- **Page** and **Items per page** – Set the page number and how many items per page.
- **Load** – Fetches that page from the API (URL will show `?page=...&limit=...`).
- **Previous** / **Next** – Go to the previous or next page. They are disabled on page 1 and the last page.
- The table shows the products for the current page. Below it you see the request URL and full JSON response.

Try changing the page (e.g. 2, 5) and the limit (e.g. 5, 20) and click Load to see how the URL and data change.

---

## Step 5: Observe SQL Behavior

On the server, each request runs something like:

- `SELECT COUNT(*) FROM products` → to get total items and compute total pages.
- `SELECT id, name, price FROM products ORDER BY id LIMIT 10 OFFSET 20` for page 3 with limit 10.

So the database only returns one page of rows, not all 100. That is what makes pagination efficient.

---

## Step 6: Test Edge Cases

**Page too high**

- Set page to 999 and click Load. You should get an empty `data` array but valid `currentPage`, `totalPages`, `totalItems`. No error.

**Page &lt; 1**

- Call the API directly: `http://127.0.0.1:5003/products?page=0`  
  You should get HTTP 400 with `"error": "page must be 1 or greater"`.

**Limit too large**

- Try `?limit=1000`. The server caps limit at 50 (MAX_LIMIT), so you get at most 50 items per page. This is **input validation**: without it, a client could request millions of rows and overload the server or network.

---

## Pagination Flow – Simple Diagram (Text)

```
  CLIENT (browser)                    SERVER (Flask)

  1. Request page 2, 10 per page
     GET /products?page=2&limit=10
     ----------------------------------------------->
                                              Read query params: page=2, limit=10
                                              total_items = SELECT COUNT(*) ...
                                              offset = (2 - 1) * 10 = 10
                                              SELECT ... LIMIT 10 OFFSET 10
     2. Response JSON:
        { currentPage: 2, totalPages: 10, totalItems: 100, itemsPerPage: 10, data: [ ... ] }
     <-----------------------------------------------
     Update table and "Current page / Total pages / Total items"
```

So: **Client** asks for a page → **Server** uses **LIMIT** and **OFFSET** in SQL → **Response** includes that page’s data plus metadata (current page, total pages, total items).

---

## Example API Request and Response

**Request (page 2, 10 per page):**

- URL: `http://127.0.0.1:5003/products?page=2&limit=10`
- Method: `GET`
- No body.

**Response (200 OK):**

```json
{
  "currentPage": 2,
  "totalPages": 10,
  "totalItems": 100,
  "itemsPerPage": 10,
  "data": [
    { "id": 11, "name": "Product 11", "price": 22.49 },
    { "id": 12, "name": "Product 12", "price": 34.99 },
    ...
  ]
}
```

**Response when page &gt; total pages (e.g. page 99):**

```json
{
  "currentPage": 99,
  "totalPages": 10,
  "totalItems": 100,
  "itemsPerPage": 10,
  "data": []
}
```

**Error when page &lt; 1 (e.g. ?page=0):**

- HTTP 400  
- Body: `{ "error": "page must be 1 or greater" }`

---

## Pagination Logic in Plain English

1. **Page number** and **limit** come from the URL query (e.g. `page=2`, `limit=10`).
2. **OFFSET** = `(page - 1) * limit`. For page 2 and limit 10, offset = 10, so we skip the first 10 rows and return the next 10.
3. **Total count** – We run `SELECT COUNT(*) FROM products` to know how many products exist. Then **totalPages** = ceil(totalItems / limit). We need this so the client can show “Page 2 of 10” and disable Next on the last page.
4. **SQL** – `SELECT ... ORDER BY id LIMIT ? OFFSET ?` returns only that page of rows. So we never load all 100 rows into memory or send them in one response.

---

## Why This Improves Performance

| Aspect        | Without pagination (all 100)     | With pagination (e.g. 10 per page)   |
|---------------|-----------------------------------|---------------------------------------|
| **Memory**    | Server holds 100 rows in memory  | Server holds 10 rows                  |
| **Network**   | One large JSON (all 100)         | Small JSON (10 items) per request     |
| **Database**  | Returns entire result set        | Stops after LIMIT rows               |
| **Browser**   | Parses and may render 100 rows   | Parses and renders 10 rows            |

So pagination improves performance on the server, network, and client. For very small datasets (e.g. 5 products), one page already contains everything, so pagination doesn’t change much – it becomes useful when you have many items (50, 100, 1000+).

---

## Why Input Validation Matters

- **page &lt; 1** – We return 400. Otherwise `(page - 1) * limit` could be negative and cause odd or broken behavior.
- **limit too large** – We cap at 50. Otherwise a client could send `?limit=1000000` and force the server and network to handle a huge response, which can slow or crash the service. Limiting `limit` protects the server and keeps responses predictable.

---

## Files in This Project

- **app.py** – Defines the `products` table, inserts 100 sample products, and implements GET /products with `page` and `limit` query parameters, LIMIT/OFFSET, edge cases, and comments.
- **templates/index.html** – Table, page/limit inputs, Load / Previous / Next, display of current page and total pages/items, and fetch() with query parameters. Comments explain query params, fetch, JSON parsing, and pagination state.
- **requirements.txt** – Flask.
- **products.db** – SQLite database (created on first run).

The goal is **conceptual clarity**, understanding **performance**, and **hands-on learning** – not production-level optimization.
