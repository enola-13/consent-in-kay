from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Regex for sensitive/personal detection
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'\b\d{8,15}\b')  # Basic phone number pattern
PASSWORD_REGEX = re.compile(r'password|pass|pwd|1234', re.IGNORECASE)

def check_sensitivity(message):
    """
    Detect message sensitivity:
    - 'sensitive' if email or password patterns
    - 'personal' if phone number
    - 'safe' otherwise
    """
    if EMAIL_REGEX.search(message) or PASSWORD_REGEX.search(message):
        return "sensitive"
    if PHONE_REGEX.search(message):
        return "personal"
    return "safe"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    message = data.get("message", "")

    sensitivity = check_sensitivity(message)
    
    # Frontend must confirm permission for sensitive messages
    allow = True
    if sensitivity == "sensitive":
        allow = data.get("allow", False)

    response = {
        "message": message if allow else "[REDACTED]",
        "sensitivity": sensitivity if allow else "safe"
    }
    return jsonify(response)

if __name__ == "__main__":
    # Debug mode on for local testing; set debug=False for production
    app.run(debug=True)
