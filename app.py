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

    def checkWireguard(self,port):

        result = subprocess.run(["nc", "-u", "-z", "-v", "-w5", self.host, str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode == 0:

            return True

        else:

            return False


    def checkPing(self):
        result = subprocess.run(["ping", "-c", "1", "-W", "2", self.host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode == 0:
            print("Ping fonctionnel")
            return True
        else:
            print("Non fonctionnel")
            return False


@app.route('/', methods=["GET"])
def main():

    monitoring = Raspberry("192.168.10.3")
    service = {
        "nginx": monitoring.checkServiceStatus(443),
        "ssh": monitoring.checkServiceStatus(22),
        "icmp": monitoring.checkPing(),
        "wireguard": monitoring.checkWireguard(65016),
        "docker - Bitwarden": monitoring.checkWireguard(8080),
        "bind": monitoring.checkWireguard(53)
    }

    if request.accept_mimetypes.best == 'application/json':
        return jsonify(service)

    return render_template("index.html", services=service, device="Raspberry - Loulax.fr")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
