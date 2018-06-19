from core.devices.input_device import InputDevice
import app_server

class AppDevice(InputDevice):
    def __init__(self, host, port):
        super(AppDevice, self).__init__()

        self.host=host
        self.port=port

    def main(self, output_devices):
        app_server.run(self.host, self.port, output_devices)