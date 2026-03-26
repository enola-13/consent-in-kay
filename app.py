from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Detect sensitive info like emails
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

def check_sensitivity(message):
    """Return message sensitivity class: safe, personal, sensitive"""
    if EMAIL_REGEX.search(message):
        return "sensitive"
    # Add other rules for personal info here if needed
    return "safe"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    message = data.get("message", "")
    
    sensitivity = check_sensitivity(message)
    
    # Ask permission for sensitive info
    allow = True
    if sensitivity == "sensitive":
        allow = data.get("allow", False)  # Frontend confirms permission
    
    response = {
        "message": message if allow else "[REDACTED]",
        "sensitivity": sensitivity if allow else "safe"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
