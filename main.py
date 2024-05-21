from flask import Flask, jsonify, render_template
import os
import json
import subprocess

app = Flask(__name__)

def get_config(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return None

def get_hosts():
    vm1 = get_config("vm1.json")
    vm2 = get_config("vm2.json")
    return {"vm1": vm1, "vm2": vm2}

def ping(host):
    result = subprocess.run(["/usr/bin/ping", "-c", "1", host], capture_output=True, text=True)
    if result.returncode == 0:
        # Extract ping time from the output
        time_index = result.stdout.find("time=")
        if time_index != -1:
            time_str = result.stdout[time_index+5:]
            time_str = time_str.split()[0]
            print(float(time_str))
            return float(time_str)
    return None   

@app.route("/api/devices", methods=["GET"])
def get_devices():
    
    devices = get_hosts()
    ping_times = {
        "vm1": ping("1.1.1.1"),
	"vm2": ping("2.2.2.2")
    }
    return jsonify({"devices": devices, 'ping_times': ping_times})

@app.route("/", methods=["GET"])
def main():
    devices = get_hosts()
    return render_template("index.html", devices=devices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
