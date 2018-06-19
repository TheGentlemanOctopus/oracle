from flask import Flask

from core.devices.input_device import InputDevice

app = Flask(__name__)
app.data = {}

@app.route('/')
def index():
    return "Hello World"

def run(in_queue, out_queue):
    app.data["in_queue"] = in_queue
    app.data["out_queue"] = out_queue

    app.run()