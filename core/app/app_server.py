from flask import Flask, render_template, request, jsonify
from multiprocessing import Queue

from core.devices.input_device import InputDevice
from core.devices.output_device import switch_animation_message, update_param_message
from core.utilities import round_to_exponent
import time
app = Flask(__name__)

# Simplest way I know share data between functions in flask is to make a data dict
app.data = {
    "output_devices": {}, # key: device name, value: device
    "fft_in_queue": None
}

def run(host, port, output_devices, fft_in_queue):
    """
        Call this function to start the server
    """
    
    app.data["output_devices"] = {device.name: device for device in output_devices} 
    app.data["fft_in_queue"] = fft_in_queue
    app.run(host=host, port=port)

@app.route('/')
def index():
    """
        Main page of controller
    """

    # Data for template rendering
    devices = [device_render_data(device) for device in app.data["output_devices"].values()]

    return render_template('index.html', 
        devices=devices, 
        fft_recorder=app.data["fft_in_queue"] is not None
    )

@app.route('/switch_animation', methods=['POST'])
def switch_animation():
    """
        Switches an animation
    """

    # Check format of POST data
    if "device_name" not in request.form:
        # TODO: log error
        return "error: device name not specified"
    device_name = request.form["device_name"]

    if request.form["device_name"] not in app.data["output_devices"]:
        # TODO: log error
        return "error: device name unknown"
    device = app.data["output_devices"][device_name]

    if "new_animation" not in request.form:
        # TODO: log error
        return "error: new animation not defined"
    new_animation_name = request.form["new_animation"]

    # Send switch message and then wait until it has been processed
    device.in_queue.put(switch_animation_message(new_animation_name))
    animation_data = device.animation_queue.get()

    return jsonify({"name": device.name, "animation": animation_data})

@app.route("/set_param", methods=["POST"])
def set_param():
    """
        Sets a parameter
    """
    if "param_name" not in request.form:
        return "no param name"
    param_name = request.form["param_name"].strip()

    if "param_value" not in request.form:
        return "no param value"
    param_value = float(request.form["param_value"])

    if "device_name" not in request.form:
        return "no device name"

    if request.form["device_name"] not in app.data["output_devices"]:
        return "unknown device name"

    device = app.data["output_devices"][request.form["device_name"]]
    device.in_queue.put(update_param_message(param_name, param_value))

    return "done"

def put_fft_in_queue(message):
    """
        Puts an item in the fft queue if there is one
    """
    if app.data["fft_in_queue"] is None:
        return

    app.data["fft_in_queue"].put(message)

@app.route("/start_record")
def start_record():
    put_fft_in_queue("start_record")
    return "done"

@app.route("/stop_record")
def stop_record():
    put_fft_in_queue("stop_record")
    return "done"

def device_render_data(device):
    # Request current animation data
    device.in_queue.put(switch_animation_message(""))

    return {
        "name": device.name,
        "possible_animations": device.possible_animations().keys(),
        "animation": device.animation_queue.get()
    }