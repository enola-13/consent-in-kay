from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Regex to detect sensitive information like emails
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

def check_sensitivity(message):
    """
    Check message for sensitive info and return status:
    'green' - safe
    'yellow' - caution
    'red' - sensitive
    """
    if EMAIL_REGEX.search(message):
        return "red"
    return "green"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.json.get("message", "")
    sensitivity = check_sensitivity(message)
    response = {
        "message": message,
        "sensitivity": sensitivity
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
