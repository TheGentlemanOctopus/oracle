'''Generates a JSON file for use with the GL simulator'''
from devices import construct_devices
import json
import sys

def main():
    devices = construct_devices(sys.argv[1])

    # Combine into one big pixels by channel
    channels_combined = {}
    for device in devices:
        for channel, pixels in device.pixels_by_channel.items():
            if channel in channels_combined:
                channels_combined[channel].extend(pixels)
            else:
                channels_combined[channel] = pixels


    # Output each one into json
    i=0
    for channel, pixels in channels_combined.items():
        i+=1
        json_data = [{"point": pixel.location} for pixel in pixels]
        
        # TODO: Temp directory thing
        with open('layout_%i.json'%i, 'w') as f:
            json.dump(json_data, f, indent=4)
    
    print "dumped", i, "channels"
    # TODO: Launch


if __name__ == '__main__':
    main()