from core.devices.input_device import InputDevice
from app_server import run

class AppDevice(InputDevice):
    def __init__(self):
        super(AppDevice, self).__init__()


    def main(self):
        run(self.in_queue, self.out_queue)