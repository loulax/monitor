#!/usr/bin/python3

import subprocess
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
class Raspberry:

    def __init__(self, host):

        self.host = host

    def checkServiceStatus(self, port):
        result = subprocess.run(["nc", "-z", "-v", "-w5", self.host, str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode == 0:
            return True
        else:
            return False


    def checkPing(self):
        result = subprocess.run(["ping", "-c", "3", "-W", "2", self.host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode == 0:
            return True
        else:
            return False

    def device(self):

        return False
    
@app.route('/', methods=["GET"])
def main():

    monitoring = Raspberry("172.18.153.240")
    service = {
        "apache": monitoring.checkServiceStatus(80),
        "ssh": monitoring.checkServiceStatus(22),
        "icmp": monitoring.checkPing(),
    }

    if request.accept_mimetypes.best == 'application/json':
        return jsonify(service)

    return render_template("index.html", services=service, device="Raspberry")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
