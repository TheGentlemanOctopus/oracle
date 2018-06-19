from flask import Flask
from multiprocessing import Queue
from core.devices.input_device import InputDevice

app = Flask(__name__)
app.data = {}

def run(output_devices, in_queue, out_queue):
    app.data["output_devices"] = output_devices 
    app.data["in_queue"] = in_queue
    app.data["out_queue"] = out_queue

    app.run()

@app.route('/')
def index():
    return "".join([device.name for device in app.data["output_devices"]])

