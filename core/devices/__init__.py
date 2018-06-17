import core.utilities.process_descriptor as pd
from output_device import OutputDevice

# To be able construct a device, all you have to is import it here 
import cube_strip
import lonely
import big_cube

# Generates dictionary with the class name as key and class as value. 
# Useful for constructing device class instances
output_device_dict = {}
for output_device in OutputDevice.__subclasses__():
    output_device_dict[output_device.__name__] = output_device

def construct_output_devices(output_devices_data_dict):
    """
        Returns a list constructed devices given a list of initialisation data
        Each element in devices_data_dict should be a dictionary with format 
        {
            "type": <name of device class>,
            "args": <dict of constructor args>
        }
    """

    # TODO: Error handling

    output_devices = []
    # Construct device from the dictionary the device_dict above
    for output_device_data in output_devices_data_dict:
        output_device_constructor = output_device_dict[output_device_data["type"]]
        output_devices.append(output_device_constructor(**output_device_data["args"]))

    return output_devices

def combine_channel_dicts(output_devices):
    """ 
        Combines channel dictionarties from a list of devices into one big one into one
        Pixels are ordered in the same order as the array
    """
    channels_combined = {}
    for output_device in output_devices:
        for channel, pixels in output_device.pixels_by_channel.items():
            if channel in channels_combined:
                channels_combined[channel].extend(pixels)
            else:
                channels_combined[channel] = pixels

    return channels_combined