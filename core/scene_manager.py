from multiprocessing import Process, Queue
import time
import opc
import sys
import numpy as np

from core.devices import construct_devices, combine_channel_dicts

class SceneManager(object):
    """docstring for SceneManager"""
    def __init__(self,  opc_host="127.0.0.1", opc_port=7890):
        opc_ip = opc_host + ":" + str(opc_port)
        self.client = opc.Client(opc_ip)

        # If the client is not connected the put_pixels operation is slow as it tries to reconnect
        if not self.client.can_connect():
            raise Exception("Could not connect to opc at " + opc_ip)

    def start(self, devices):
        device_pixel_dictionary_list = [device.pixels_by_channel_255 for device in devices]

        # Start Processes
        for device in devices:
            p = Process(target=device.main)
            p.start()

        # Recombine
        while True:
            # Update pixel lists if new data has arrived
            for i, device in enumerate(devices):
                if not device.out_queue.empty():
                    device_pixel_dictionary_list[i] = device.out_queue.get()

            # Combine
            channels_combined = {}
            for pixel_dict in device_pixel_dictionary_list:
                for channel, pixels in pixel_dict.items():
                    if channel in channels_combined:
                        channels_combined[channel].extend(pixels)
                    else:
                        channels_combined[channel] = [p for p in pixels]
            
            # Pass onto OPC client
            for channel, pixels in channels_combined.items():
                self.client.put_pixels(pixels, channel=channel)


if __name__ == '__main__':
    devices = construct_devices(sys.argv[1])

    scene = SceneManager()
    scene.start(devices)