from flask import Flask, render_template
from multiprocessing import Queue
from core.devices.input_device import InputDevice

app = Flask(__name__)
app.data = {"output_devices": []}

def run(host, port, output_devices):
    app.data["output_devices"] = output_devices 
    app.run(host=host, port=port)


@app.route('/')
def index():
    devices = [{
        "name": device.name,
        "possible_animations": [a for a in device.possible_animations()]
    } for device in app.data["output_devices"]]

    print "POSSOS", devices[0]["possible_animations"]

    return render_template('index.html', devices=devices)

