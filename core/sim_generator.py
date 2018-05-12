'''Generates a JSON file for use with the GL simulator'''
from lonely import Lonely
from cube_strip import CubeStrip
from scene_manager import construct_devices
import json
import sys

def main():

    devices = construct_devices(sys.argv[1])
    
    pixels = []
    for device in devices:
        pixels.extend(device.pixels)

    json_data = [{"point": pixel.location} for pixel in pixels]
    with open('lonely_layout.json', 'w') as f:
        json.dump(json_data, f)
    print "dumped"

if __name__ == '__main__':
    main()