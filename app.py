#!/usr/bin/python3

import subprocess
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
class Monitor:

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

# Votre code pour la classe Monitor et les fonctions de surveillance

# Définition des devices et des services à surveiller
devices = {
    "raspberry": Monitor("10.10.10.2"),
    "server2": Monitor("10.10.10.3")
}

services_to_monitor = {
    "raspberry": [
        {"name": "nginx", "port": 80},
        {"name": "ssh", "port": 2221},
    ],
    "server2": [
        {"name": "ssh", "port": 2222},
        {"name": "apache", "port": 80},
    ],
}

@app.route('/', methods=["GET"])
def main():
    device_name = request.args.get('device')  # Récupérer le nom de l'appareil depuis les paramètres de requête

    if device_name:
        device = devices.get(device_name)
        if device is None:
            return render_template("404.html"), 404

        services = {}
        for service in services_to_monitor.get(device_name, []):
            if "port" in service:
                services[service["name"]] = device.checkServiceStatus(service["port"])
            else:
                services[service["name"]] = device.checkPing()

        if request.accept_mimetypes.best == 'application/json':
            return jsonify(device_name, services)

        return render_template("index.html", device=device_name, services=services)
    else:
        # Logique pour la page d'accueil par défaut
        data = {}
        for device_name, device in devices.items():
            services = {}
            for service in services_to_monitor.get(device_name, []):
                if "port" in service:
                    services[service["name"]] = device.checkServiceStatus(service["port"])
                else:
                    services[service["name"]] = device.checkPing()
            data[device_name] = {"services": services}

        if request.accept_mimetypes.best == 'application/json':
            return jsonify(data)

        return render_template("index.html", devices=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)