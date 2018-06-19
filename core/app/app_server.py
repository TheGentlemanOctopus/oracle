from flask import Flask, render_template, request
from multiprocessing import Queue

from core.devices.input_device import InputDevice
from core.devices.output_device import switch_animation_message

app = Flask(__name__)
app.data = {
    "output_devices": {} # key: device name, value: device
}

def run(host, port, output_devices):
    app.data["output_devices"] = {device.name: device for device in output_devices} 
    app.run(host=host, port=port)

@app.route('/')
def index():
    devices = [{
        "name": name,
        "possible_animations": [a for a in device.possible_animations()]
    } for (name, device) in app.data["output_devices"].items()]

    return render_template('index.html', devices=devices)

@app.route('/switch_animation', methods=['GET', 'POST'])
def switch_animation():
    if "device_name" not in request.form:
        # TODO: log error
        return
    device_name = request.form["device_name"]

    if request.form["device_name"] not in app.data["output_devices"]:
        # TODO: log error
        return
    device = app.data["output_devices"][device_name]

    if "new_animation" not in request.form:
        # TODO: log error
        return
    new_animation_name = request.form["new_animation"]

    # switch it up
    device.in_queue.put(switch_animation_message(new_animation_name))

    

