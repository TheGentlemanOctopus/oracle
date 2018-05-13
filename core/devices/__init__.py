import core.utilities.process_descriptor as pd
from device import Device

# To be able construct a device, all you have to is import it here 
import cube_strip
import lonely

# Generates dictionary with class name as key and class as value. 
# Useful for constructing device class instances
device_dict = {}
for device in Device.__subclasses__():
    device_dict[device.__name__] = device


def construct_devices(scene_descriptor_path):
    # TODO: Error handling for json format

    # Load JSON
    json_data = pd.process(scene_descriptor_path)

    devices = []
    # Construct device from the dictionary of device classes that are keyed by their __name__
    for device_json in json_data["OutputDevices"]:
        device_constructor = device_dict[device_json["type"]]
        devices.append(device_constructor(**device_json["args"]))

    return devices

def combine_channel_dicts(devices):
    """ 
        Combines channel dictionarties from a list of devices into one big one into one
        Pixels are ordered in the same order as the array
    """
    channels_combined = {}
    for device in devices:
        for channel, pixels in device.pixels_by_channel.items():
            if channel in channels_combined:
                channels_combined[channel].extend(pixels)
            else:
                channels_combined[channel] = pixels

    return channels_combined