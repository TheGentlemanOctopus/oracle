from multiprocessing import Process, Queue
import time
import opc
import sys

from core.devices import construct_devices

class SceneManager(object):
    """docstring for SceneManager"""
    def __init__(self,  opc_host="127.0.0.1", opc_port=7890):
        opc_ip = opc_host + ":" + str(opc_port)
        self.client = opc.Client(opc_ip)

        # If the client is not connected the put_pixels operation is slow as it tries to reconnect
        if not self.client.can_connect():
            raise Exception("Could not connect to opc at " + opc_ip)

    def start(self, devices):
        for device in devices:
            p = Process(target=device.main)
            p.start()

        while True:
            # TODO: This assumes each device has a unique set of channels
            # TODO: This only works with gl server,
            # Combine pixels across all devices by channel
            all_pixels_dict = {}
            for device in devices:
                for channel, pixels in device.out_queue.get().items():
                    all_pixels_dict[channel] = pixels
                    
            # Send to client
            all_pixels_list = []
            for channel in sorted(all_pixels_dict.keys()):
                all_pixels_list.extend(all_pixels_dict[channel])

            self.client.put_pixels(all_pixels_list, channel=0)


if __name__ == '__main__':
    devices = construct_devices(sys.argv[1])

    scene = SceneManager()
    scene.start(devices)