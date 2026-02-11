from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

items = []
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_item", methods=["POST"])
def add_item():
    new_item = request.json.get("item") 
    if new_item:
        items.append(new_item) 
        return jsonify({"success": True, "items": items})
    list
    return jsonify({"success": False, "error": "No item provided"})

if __name__ == "__main__":
    app.run(debug=True)