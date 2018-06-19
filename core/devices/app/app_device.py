from core.devices.input_device import InputDevice
import app_server

class AppDevice(InputDevice):
    def __init__(self):
        super(AppDevice, self).__init__()

    def main(self, output_devices):
        app_server.run(output_devices, self.in_queue, self.out_queue)

