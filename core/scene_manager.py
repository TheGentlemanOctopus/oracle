from multiprocessing import Process, Queue
import time
import opc
import sys
import numpy as np
import utilities.process_descriptor as pd

from core.devices import construct_devices, combine_channel_dicts

class SceneManager(object):
    """docstring for SceneManager"""
    def __init__(self, 
                scene_fps=60, 
                device_fps=30, 
                opc_host="127.0.0.1", 
                opc_port=7890
        ):
        opc_ip = opc_host + ":" + str(opc_port)
        self.client = opc.Client(opc_ip)

        # If the client is not connected the put_pixels operation is slow as it tries to reconnect
        if not self.client.can_connect():
            raise Exception("Could not connect to opc at " + opc_ip)

        self.scene_fps = scene_fps
        self.device_fps = device_fps



    def start(self, devices):

        device_pixel_dictionary_list = [device.pixels_by_channel_255 for device in devices]

        # Start Processes
        for device in devices:
            device.fps = self.device_fps
            p = Process(target=device.main)
            p.start()

        # Recombine
        while True:
            loop_time = time.time()
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

            # The scene_fps should be at least 2x device_fps to avoid sampling issues
            elapsed = time.time() - loop_time
            sleep_time = (1.0/self.scene_fps) - elapsed
            if sleep_time < 0: 
                sleep_time = 0
            time.sleep(sleep_time)


if __name__ == '__main__':
    parsed = pd.read_json(sys.argv[1])

    devices = construct_devices(sys.argv[1])

    scene = SceneManager(**parsed["SceneDetails"])
    scene.start(devices)