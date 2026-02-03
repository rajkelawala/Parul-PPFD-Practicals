from flask import Flask, render_template, request
app = Flask(__name__)

# Route for the home page with the input form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input from the form
        user_input = request.form["user_input"]
        # Process the input (in this case, reverse the string)
        processed_data = user_input[::-1]
        # Pass the processed data to the result template
        return render_template("result.html", original=user_input,                           result=processed_data)
    # Render the form on GET request
    return render_template("input.html")

if __name__ == "__main__":
    app.run(debug=True)