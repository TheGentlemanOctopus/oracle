'''Generates a JSON file for use with the GL simulator'''
from lonely import Lonely
import json

def main():
    devices = [Lonely()]
    pixels = []
    for device in devices:
        pixels.extend(device.pixels)

    json_data = [{"point": pixel.location} for pixel in pixels]
    with open('lonely_layout.json', 'w') as f:
        json.dump(json_data, f)

if __name__ == '__main__':
    main()