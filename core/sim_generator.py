'''Generates a JSON file and launches GL simulator given the layout'''
from devices import construct_devices, combine_channel_dicts
import json
import sys
import os
import subprocess

def main():
    devices = construct_devices(sys.argv[1])

    channels_combined = combine_channel_dicts(devices)

    # Make temp folder 
    temp_dir = os.path.dirname(os.path.abspath( __file__ )) + "/temp/"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    json_filenames = []

    # Output each channel into a json
    i=0
    for channel, pixels in channels_combined.items():
        i+=1
        json_data = [{"point": pixel.location} for pixel in pixels]
        
        json_filename = temp_dir + 'layout_%i.json'%i
        json_filenames.append(json_filename)

        with open(json_filename, 'w') as f:
            json.dump(json_data, f, indent=4)

    command = ["gl_server"]
    for filename in json_filenames:
        command.append("-l")
        command.append(filename)

    print "Launching gl_server", command
    subprocess.call(command)



if __name__ == '__main__':
    main()