from multiprocessing import Process, Queue, Lock
import time
import opc
import sys
import numpy as np
import utilities.process_descriptor as pd
from utilities.sleep_timer import SleepTimer
import argparse

from core.devices import construct_devices, combine_channel_dicts

class SceneManager(object):
    """
        Scene Manager is responsible for running a scene
        Runs a set of devices (currently only output devices), combines pixel data and forwards onto server
        TODO: Handling for input devices
    """
    def __init__(self, 
            scene_fps=60, 
            device_fps=30, 
            opc_host="127.0.0.1", 
            opc_port=7890
        ):
        """
            Initialisation connects to the opc server
            Note: This does not run device processes, that's the job of the start command
        """

        # Connect to opc client
        opc_ip = opc_host + ":" + str(opc_port)
        self.client = opc.Client(opc_ip)

        if not self.client.can_connect():
            raise Exception("Could not connect to opc at " + opc_ip)

        # Set fps for scene and device
        self.scene_fps = scene_fps
        self.device_fps = device_fps

    def start(self, devices):
        """
            Runs the scene forever. 
            devices is a list of device objects
        """

        # A list of dictionaries which are the device's pixel colors by channel
        # Serves as a reference of all the scene pixel colors that get sent to opc in the loop
        device_pixel_dictionary_list = [device.pixel_colors_by_channel_255 for device in devices]

        # Start Processes
        for device in devices:
            device.fps = self.device_fps
            p = Process(target=device.main)
            p.start()

        # Main loop
        sleep_timer = SleepTimer(1.0/self.scene_fps)
        while True:
            sleep_timer.start()
            
            # Update pixel lists if new data has arrived
            for i, device in enumerate(devices):

                # Get the device queue mutex
                with device.queue_mutex:
                    if not device.out_queue.empty():
                        device_pixel_dictionary_list[i] = device.out_queue.get()
    
            # Combine the scene pixels into one concatenated dictionary keyed by channel number
            # Multiple devices using the same channel are combined with the same ordering as the devices list
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
            # TODO: comment above shouldn't be necessary, I think the queue clear in devices requires a mutex
            sleep_timer.sleep()

def main(args):
    # Parse Args
    parser = argparse.ArgumentParser(description="Run a scene for us all to marvel")
    parser.add_argument("scene_path", help="Path to scene json file")   
    parser_args = parser.parse_args(args)

    parsed_scene = pd.read_json(parser_args.scene_path)

    # Prepare for scene time...
    scene = SceneManager(**parsed_scene["SceneDetails"])
    devices = construct_devices(parsed_scene["OutputDevices"])

    # Yaaay! Scene time
    scene.start(devices)

if __name__ == '__main__':
    main(sys.argv[1:])
