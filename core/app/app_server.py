from flask import Flask, render_template, request
from multiprocessing import Queue

from core.devices.input_device import InputDevice
from core.devices.output_device import switch_animation_message

app = Flask(__name__)

# Simplest way I know share data between functions in flask is to make a data dict
app.data = {
    "output_devices": {} # key: device name, value: device
}

def run(host, port, output_devices):
    """
        Call this function to start the server
    """
    
    app.data["output_devices"] = {device.name: device for device in output_devices} 
    app.run(host=host, port=port)

@app.route('/')
def index():
    """
        Main page of controller
    """

    # Data for template rendering
    devices = [{
        "name": name,
        "possible_animations": device.possible_animations(),
        "animation": animation_data(device.animation)
    } for (name, device) in app.data["output_devices"].items()]

    return render_template('index.html', devices=devices)

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

    # switch it up
    message = switch_animation_message(new_animation_name)
    
    # Send switch message and then wait until it has been processed
    with device.animation_cv:
        device.in_queue.put(message)
        device.animation_cv.wait()

    return "done"    

def animation_data(animation):
    return {
        "name": animation.__class__.__name__,
        "params": [{
            "name": name,
            "min": param.min,
            "max": param.max,
            "value": param.value,
            "step": (param.max - param.min)/30.0
        } for (name, param) in animation.params.items()]
    }



