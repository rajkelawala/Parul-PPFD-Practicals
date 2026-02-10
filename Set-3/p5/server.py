from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        processed_data = user_input[::-1]
        return render_template("result.html", original=user_input,                           result=processed_data)
    return render_template("input.html")

if __name__ == "__main__":
    app.run(debug=True)