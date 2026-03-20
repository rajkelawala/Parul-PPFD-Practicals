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
