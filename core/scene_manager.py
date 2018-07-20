from multiprocessing import Process, Queue, Lock
from Queue import Empty
import time
import opc
import sys
import numpy as np
import utilities.process_descriptor as pd
from utilities.sleep_timer import SleepTimer
import core.utilities.logging_server

import argparse

from core.devices.fft_device import FftDevice
from core.devices import construct_output_devices, construct_input_devices, combine_channel_dicts
from core.devices.app_device import AppDevice

class SceneManager(object):
    """
        Scene Manager is responsible for running a scene
        Runs a set of devices (currently only output devices), combines pixel data and forwards onto server
        TODO: Handling for input devices
    """
    def __init__(self,
            input_devices,
            output_devices,
            scene_fps=60, 
            device_fps=30, 
            opc_host="127.0.0.1", 
            opc_port=7890,
            r_scaling = 0.5,
            g_scaling = 0.5,
            b_scaling = 0.5
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

        self.input_devices = input_devices
        self.output_devices = output_devices

        self.scaling = np.array([r_scaling, g_scaling, b_scaling])

        # A list of dictionaries which are the device's pixel colors by channel
        # Serves as a reference of all the scene pixel colors that get sent to opc in the loop
        self.output_device_pixel_dictionary_list = [device.pixel_colors_by_channel_255 for device in self.output_devices]

    def start(self):
        """
            Runs the scene forever. 
            devices is a list of device objects
        """
        # Initialise
        self.start_input_devices()
        self.start_output_devices()

        # Main loop
        sleep_timer = SleepTimer(1.0/self.scene_fps)
        while True:
            sleep_timer.start()
            
            self.process_input_devices()
            self.process_output_devices()
            self.update_opc()

            sleep_timer.sleep()

        # TODO: kill input/output device processes

    def start_output_devices(self):
        """
            Start output device processes
        """
        for device in self.output_devices:
            device.fps = self.device_fps
            device.start()

    def start_input_devices(self):  
        """
            Start input device processes
        """
        # HACK: Need a more generic way to share queues between devices
        # App device must be specified after fft in this way
        fft_in_queue = None

        for device in self.input_devices:
            if type(device) == AppDevice:
                device.start(self.output_devices, fft_in_queue)

            elif type(device) == FftDevice:
                fft_in_queue = device.in_queue
                device.start()

            else:
                # Assume start takes no args by default
                device.start()

    def process_input_devices(self):
        """
            Gets data from input devices and passes them onto output devices
            TODO: broadcast to specific devices
        """

        for input_device in self.input_devices:
            # Get data from the queue until cleared
            while True:
                item = input_device.get_out_queue()

                if item is None:
                    break

                # Pass onto output devices
                for output_device in self.output_devices:
                    output_device.in_queue.put(item)

    def process_output_devices(self):
        """
            Retrieve pixels from all output devices
        """

        # Update pixel lists if new data has arrived
        for i, device in enumerate(self.output_devices):
            # Get the device queue mutex
            with device.queue_mutex:
                pixel_dict = device.get_out_queue()

                if pixel_dict:
                    self.output_device_pixel_dictionary_list[i] = pixel_dict

    def update_opc(self):
        """
            Sends the latest pixels to opc
        """
        # Combine the scene pixels into one concatenated dictionary keyed by channel number
        # Multiple devices using the same channel are combined with the same ordering as the devices list
        channels_combined = {}
        for pixel_dict in self.output_device_pixel_dictionary_list:
            for channel, pixels in pixel_dict.items():
                if channel in channels_combined:
                    channels_combined[channel].extend(pixels)
                else:
                    channels_combined[channel] = [p for p in pixels]

        # Pass onto OPC client
        for channel, pixels in channels_combined.items():
            scaled_pixels = np.array(np.array(pixels) * self.scaling).astype(int)
            self.client.put_pixels(scaled_pixels, channel=channel)

def run_scene(scene_path):
    """
        Runs a scene from a scene path
    """
    parsed_scene = pd.read_json(scene_path)

    # Form devices
    input_devices = construct_input_devices(parsed_scene["InputDevices"])
    output_devices = construct_output_devices(parsed_scene["OutputDevices"])
    
    scene = SceneManager(input_devices, output_devices, **parsed_scene["SceneDetails"])

    # Yaaay! Scene time
    scene.start()

def main(args):
    # Parse Args
    parser = argparse.ArgumentParser(description="Run a scene for us all to marvel")
    parser.add_argument("scene_path", help="Path to scene json file")   
    parser_args = parser.parse_args(args)

    # Start the logging server
    logging_process = Process(target=core.utilities.logging_server.main)
    logging_process.daemon = True
    logging_process.start()

    run_scene(parser_args.scene_path)


if __name__ == '__main__':
    main(sys.argv[1:])
