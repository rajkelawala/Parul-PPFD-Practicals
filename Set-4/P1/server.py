from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    items = [
        {"name": "Apple", "price": "$1.00"},
        {"name": "Banana", "price": "$0.50"},
        {"name": "Cherry", "price": "$2.00"},
        {"name": "Date", "price": "$3.00"},
        {"name": "Elderberry", "price": "$4.50"},
    ]
    return render_template("dynamic.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)
