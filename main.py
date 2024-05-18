from flask import Flask, render_template, jsonify
import os
import json

app = Flask(__name__)

def get_config(file: bool) -> bool:

    Success = True

    if os.path.exists(file):
        
        with open(file, "r")  as f:

            return json.load(f)
        
    else:

        Success = False

    return Success

def get_hosts():

    vm1 = get_config("vm1.json")
    vm2 = get_config("vm2.json")
    return vm1, vm2
    

@app.route("/", methods=["GET"])

def main():

    devices = get_hosts()

    print(devices)

    return render_template("index.html", devices=devices)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8080, debug=True)
