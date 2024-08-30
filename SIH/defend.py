from flask import Flask, request, jsonify
import json
from time import time

app = Flask(__name__)

# Configuration
BLOCK_DURATION = 300  # Block duration in seconds (5 minutes)
ATTACKERS_LOG_FILE = 'attackers_log.json'  # File to read attacker info from

# Load attackers data from JSON file
def load_attackers():
    try:
        with open(ATTACKERS_LOG_FILE, 'r') as json_file:
            return json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Check if an IP is currently blocked
def is_blocked(ip_address, attackers):
    if ip_address in attackers:
        current_time = time()
        last_detected = attackers[ip_address]['last_detected']
        # Check if the block duration has passed
        if current_time - last_detected < BLOCK_DURATION:
            return True
    return False

@app.route('/')
def index():
    ip_address = request.remote_addr
    attackers = load_attackers()

    # Check if the IP is blocked
    if is_blocked(ip_address, attackers):
        return jsonify({'error': 'Access denied. Your IP is temporarily blocked due to suspicious activity.'}), 403

    return "Welcome to the website!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
