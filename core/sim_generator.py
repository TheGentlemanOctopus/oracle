'''Generates a JSON file for use with the GL simulator'''
from devices import construct_devices
import json
import sys

def main():
    devices = construct_devices(sys.argv[1])
    
    pixels = []
    # TODO: Order this across all devices
    for device in devices:
        for channel in sorted(device.pixels_by_channel.keys()):
            pixels.extend(device.pixels_by_channel[channel])

    json_data = [{"point": pixel.location} for pixel in pixels]
    with open('lonely_layout.json', 'w') as f:
        json.dump(json_data, f)
    print "dumped"

if __name__ == '__main__':
    main()