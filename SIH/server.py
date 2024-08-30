from flask import Flask, request, render_template
from collections import defaultdict
from time import time, strftime, localtime
import sys

app = Flask(__name__)

# Store traffic data
traffic_data = {
    'total_requests': 0,
    'ip_requests': defaultdict(int),
    'last_request_time': defaultdict(float)
}

# Configuration: Crash after a certain number of requests
CRASH_THRESHOLD = 1000

# Filter to format timestamp
@app.template_filter('format_time')
def format_time_filter(timestamp):
    return strftime('%Y-%m-%d %H:%M:%S', localtime(timestamp))

@app.route('/')
def index():
    ip_address = request.remote_addr
    current_time = time()

    # Update traffic data
    traffic_data['total_requests'] += 1
    traffic_data['ip_requests'][ip_address] += 1
    traffic_data['last_request_time'][ip_address] = current_time

    # Crash the server if total requests exceed the threshold
    if traffic_data['total_requests'] > CRASH_THRESHOLD:
        crash_server()

    return "Welcome to the website!"

@app.route('/traffic')
def traffic():
    return render_template(
        'traffic.html',
        total_requests=traffic_data['total_requests'],
        ip_requests=traffic_data['ip_requests'],
        last_request_time=traffic_data['last_request_time']
    )

def crash_server():
    """Crash the server by consuming memory."""
    print("Server is crashing due to high traffic!", file=sys.stderr)
    # Allocate a large amount of memory to force a crash
    memory_hog = [0] * (10**8)
    return "Server crashed!", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
