"""
Prac4: Pagination in REST APIs
==================================================

What is PAGINATION?
  Pagination means splitting a large list of results into smaller "pages". Instead of
  sending 1000 products at once, we send 10 (or 20) per request. The client asks for
  "page 2" or "page 3" to get the next chunk. This makes the API faster and uses less
  memory and network.

Why is RETURNING ALL RECORDS inefficient?
  - Memory: The server must load every row into memory. With 100,000 rows, that can
    be huge. With pagination we only load one page (e.g. 10 rows).
  - Network: Sending 100,000 rows as JSON makes a very large response. Slow to send
    and slow for the browser to parse. Pagination keeps each response small.
  - Database: The database can stop after reading LIMIT rows instead of scanning
    the whole table. So pagination improves performance on the server, network, and client.

What is LIMIT?
  LIMIT is a SQL keyword that tells the database: "Return at most this many rows."
  Example: SELECT * FROM products LIMIT 10 → only 10 rows.

What is OFFSET?
  OFFSET is a SQL keyword that tells the database: "Skip this many rows, then return
  the next LIMIT rows." Example: OFFSET 20 means skip the first 20 rows. So
  LIMIT 10 OFFSET 20 gives you rows 21–30. We use it to implement "page 2", "page 3", etc.

What is a QUERY PARAMETER?
  Query parameters appear after ? in the URL. Example: /products?page=2&limit=10
  Here "page" and "limit" are query parameters. The server reads them to know which
  page to return. They are part of the URL, not the request body.

What is PAGE NUMBER?
  The page the client wants. Page 1 = first chunk, page 2 = second chunk, etc.
  We convert page number to OFFSET: page 1 → skip 0, page 2 → skip 10 (if limit=10).

What is PAGE SIZE (limit)?
  How many items per page. Often called "limit" or "page size". Default might be 10 or 20.

Why pagination is useless with very small datasets:
  If you have only 5 products, splitting into "pages of 10" still returns all 5 on page 1.
  Pagination helps when there are many rows (e.g. 50, 100, 1000+). That's why we insert
  100 sample products here – so you can see the difference between pages.

Performance comparison (conceptual):
  - Without pagination: GET /products returns all 100 products. One big JSON, more memory,
    bigger network payload. Browser must render 100 rows.
  - With pagination: GET /products?page=1&limit=10 returns 10 products. Small JSON,
    less memory, small payload. User sees page 1; clicking "Next" loads page 2.
"""

import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
DATABASE = "products.db"

# Maximum allowed limit. Prevents someone asking for limit=100000 and hurting performance.
# Input validation matters: without it, a client could request millions of rows and
# overload the server or network.
MAX_LIMIT = 50


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Create products table and insert 100 sample records so pagination is visible."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    cursor = conn.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Insert 100 products: "Product 1", "Product 2", ... with prices 9.99, 19.99, ...
        for i in range(1, 101):
            name = "Product " + str(i)
            price = round(9.99 + (i % 20) * 2.5, 2)  # Variety of prices
            conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()


# ----- GET /products (paginated) -----
@app.route("/products", methods=["GET"])
def get_products():
    """
    Return products for the requested page.
    Query parameters:
      - page: which page (default 1). Page 1 = first chunk.
      - limit: how many items per page (default 10). Capped at MAX_LIMIT.
    Uses SQL LIMIT and OFFSET to fetch only one page of rows.
    """
    # request.args contains query parameters from the URL. Example: ?page=2&limit=10
    page_param = request.args.get("page", "1")
    limit_param = request.args.get("limit", "10")

    # Convert to integers. If invalid, use defaults.
    try:
        page = int(page_param)
    except ValueError:
        page = 1
    try:
        limit = int(limit_param)
    except ValueError:
        limit = 10

    # Edge case: page must be at least 1. Otherwise return error.
    if page < 1:
        return jsonify({"error": "page must be 1 or greater"}), 400

    # Edge case: limit too large. Restrict to MAX_LIMIT so one request cannot fetch too much.
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT
    if limit < 1:
        limit = 10

    conn = get_db_connection()

    # We need total count to compute totalPages. This is a separate query.
    # Why? Because we need to know "how many products exist in total" to show
    # "Page 2 of 10". Without a count we cannot tell the client how many pages there are.
    total_items = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    # Total pages = ceil(total_items / limit). Example: 100 items, limit 10 → 10 pages.
    total_pages = (total_items + limit - 1) // limit if total_items > 0 else 1

    # OFFSET = how many rows to skip. Page 1 → skip 0; page 2 → skip 10; page 3 → skip 20.
    # Formula: (page - 1) * limit. So we only read one page of rows from the database.
    offset = (page - 1) * limit

    # If page number is beyond the last page, return empty data (no error, just no items).
    if page > total_pages:
        conn.close()
        return jsonify({
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items,
            "itemsPerPage": limit,
            "data": []
        })

    # SQL: get only this page of rows. LIMIT = how many, OFFSET = how many to skip.
    # This improves performance: we never load all 100 rows into memory or send them
    # over the network in one response.
    rows = conn.execute(
        "SELECT id, name, price FROM products ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    conn.close()

    data = [{"id": r["id"], "name": r["name"], "price": r["price"]} for r in rows]

    return jsonify({
        "currentPage": page,
        "totalPages": total_pages,
        "totalItems": total_items,
        "itemsPerPage": limit,
        "data": data,
    })


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    init_database()
    app.run(host="0.0.0.0", port=5003, debug=True, use_reloader=False)
