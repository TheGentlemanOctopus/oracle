'''Generates a JSON file and launches GL simulator given the layout'''
from devices import construct_devices, combine_channel_dicts
import json
import sys
import os
import subprocess
import numpy as np

temp_dir = os.path.dirname(os.path.abspath( __file__ )) + "/temp/"

def main():
    devices = construct_devices(sys.argv[1])

    channels_combined = combine_channel_dicts(devices)

    # Make temp folder 
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    max_channels = max(channels_combined.keys())

    for i in np.arange(max_channels)+1:
        with open(json_filename(i), 'w') as f:
            json.dump({}, f, indent=4)

    # Output each channel into a json
    for channel, pixels in channels_combined.items():
        json_data = [{"point": pixel.location} for pixel in pixels]   

        with open(json_filename(channel), 'w') as f:
            json.dump(json_data, f, indent=4)

    command = ["gl_server"]
    for i in np.arange(max_channels)+1:
        command.append("-l")
        command.append(json_filename(i))

    print "Launching gl_server", command
    subprocess.call(command)

def json_filename(channel):
    return temp_dir + 'layout_%i.json'%channel


if __name__ == '__main__':
    main()