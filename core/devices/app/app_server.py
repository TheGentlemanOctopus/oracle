from flask import Flask
from multiprocessing import Queue
from core.devices.input_device import InputDevice

app = Flask(__name__)
app.data = {"output_devices": []}

def run(host, port, output_devices):
    app.data["output_devices"] = output_devices 
    app.run(host=host, port=port)

@app.route('/')
def index():
    return "".join([device.name for device in app.data["output_devices"]])

