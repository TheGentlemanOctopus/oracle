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
    device_names = [device.name for device in app.data["output_devices"]]

    return render_template('index.html', device_names=device_names)

