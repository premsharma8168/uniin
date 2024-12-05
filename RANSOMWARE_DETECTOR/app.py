from flask import Flask, render_template, jsonify
import os
import psutil
import math
import time
from collections import Counter

app = Flask(__name__)

# Threat Detection Variables
THREAT_LOG = []
SUSPICIOUS_EXTENSIONS = [".exe", ".dll", ".js", ".vbs", ".scr", ".bat"]

# Function to calculate file entropy
def calculate_file_entropy(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    if not data:
        return 0
    freq = Counter(data)
    length = len(data)
    return -sum((count / length) * math.log2(count / length) for count in freq.values())

# Scan for suspicious files
def scan_directory(directory):
    global THREAT_LOG
    threat_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                extension = os.path.splitext(file)[1].lower()
                entropy = calculate_file_entropy(filepath)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)

                if extension in SUSPICIOUS_EXTENSIONS or entropy > 7.5 or size_mb > 10:
                    THREAT_LOG.append({
                        "file": filepath,
                        "extension": extension,
                        "entropy": round(entropy, 2),
                        "size_mb": round(size_mb, 2),
                        "detected_at": time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    threat_count += 1
            except Exception:
                pass

    return threat_count

# System resource monitoring
def get_system_resources():
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }


import platform
import socket

# System information
def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "release": platform.release(),
        "ip_address": socket.gethostbyname(socket.gethostname())
    }

@app.route('/')
def dashboard():
    resources = get_system_resources()
    system_info = get_system_info()
    return render_template('index.html', resources=resources, system_info=system_info, threats=THREAT_LOG)

@app.route('/scan')
def trigger_scan():
    threat_count = scan_directory('.')  # Current directory for demonstration
    return jsonify({"status": "completed", "threats_found": threat_count})

@app.route('/api/resources')
def api_resources():
    return jsonify(get_system_resources())

@app.route('/api/threats')
def api_threats():
    return jsonify(THREAT_LOG)

if __name__ == '__main__':
    app.run(debug=True)
