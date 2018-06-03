import core.utilities.process_descriptor as pd
from device import Device

# To be able construct a device, all you have to is import it here 
import cube_strip
import lonely
import big_cube
import strip_panel

# Generates dictionary with the class name as key and class as value. 
# Useful for constructing device class instances
device_dict = {}
for device in Device.__subclasses__():
    device_dict[device.__name__] = device

def construct_devices(devices_data_dict):
    """
        Returns a list constructed devices given a list of initialisation data
        Each element in devices_data_dict should be a dictionary with format 
        {
            "type": <name of device class>,
            "args": <dict of constructor args>
        }
    """

    # TODO: Error handling

    devices = []
    # Construct device from the dictionary the device_dict above
    for device_data in devices_data_dict:
        device_constructor = device_dict[device_data["type"]]
        devices.append(device_constructor(**device_data["args"]))

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