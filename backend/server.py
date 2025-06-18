# server.py
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/run-script", methods=["POST"])
def run_script():
    data = request.json
    result = subprocess.run(["python3", "world-food-facts-api.py", data["arg"]], capture_output=True, text=True)
    return jsonify(output=result.stdout)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

