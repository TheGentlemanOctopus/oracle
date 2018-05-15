"""
    Launches the GL simulator given the scene, creating the json files it needs in a temp dir
    Expects gl_server to be on the search path
"""

from devices import construct_devices, combine_channel_dicts
import utilities.process_descriptor as pd

import json
import sys
import os
import subprocess
import numpy as np

import argparse

# directory for storing json files needed for gl_server for rendering
# (it's the same directory as this file)
temp_dir = os.path.dirname(os.path.abspath( __file__ )) + "/temp/"

def json_filepath(channel):
    """
        generates a filepath for gl_server json
    """
    return temp_dir + 'layout_%i.json'%channel

def main(args):
    # Parse Args
    parser = argparse.ArgumentParser(description="Launch the gl_server (expects gl_server to be on the search path)")
    parser.add_argument("scene_path", help="Path to scene json")   
    parser_args = parser.parse_args(args)

    scene_data = pd.read_json(parser_args.scene_path)

    # construct devices and combine into one big dict
    devices = construct_devices(scene_data["OutputDevices"])
    channels_combined = combine_channel_dicts(devices)

    # gl_server requires a json file for every channel, even if they have no pixels
    # this ensures there is a json file for every channel
    max_channels = max(channels_combined.keys())

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for i in np.arange(max_channels)+1:
        with open(json_filepath(i), 'w') as f:
            json.dump({}, f, indent=4)

    # Output each channel into a json
    for channel, pixels in channels_combined.items():
        json_data = [{"point": pixel.location} for pixel in pixels]   

        with open(json_filepath(channel), 'w') as f:
            json.dump(json_data, f, indent=4)

    # Launch gl_server with ref to the generated json
    command = ["gl_server"]
    for i in np.arange(max_channels)+1:
        command.append("-l")
        command.append(json_filepath(i))

    print "Launching gl_server", command
    subprocess.call(command)

if __name__ == '__main__':
    main(sys.argv[1:])