'''Generates a JSON file for use with the GL simulator'''
from lonely import Lonely
from cube_strip import CubeStrip

import json

def main():
    start = [0,0,0]
    direction = [1,0,0]
    spacing = 0.2
    num_pixels = 10
    devices = [
        CubeStrip(start, direction, spacing, num_pixels)
    ]
    
    pixels = []
    for device in devices:
        pixels.extend(device.pixels)

    json_data = [{"point": pixel.location} for pixel in pixels]
    with open('lonely_layout.json', 'w') as f:
        json.dump(json_data, f)

if __name__ == '__main__':
    main()