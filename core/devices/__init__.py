import core.utilities.process_descriptor as pd
from output_device import OutputDevice
from input_device import InputDevice

# To be able construct a device, all you have to is import it here 
import cube_strip
import lonely
import big_cube_device
import fft_device
import app_device
import wonderface_device
import point_cloud_device
import audio_device

# Returns a list constructed devices given a list of initialisation data
def construct_output_devices(output_devices_data_dict):
    return construct_devices(output_devices_data_dict, constructor_dict(OutputDevice))

def construct_input_devices(input_devices_data_dict):
    return construct_devices(input_devices_data_dict, constructor_dict(InputDevice))

def constructor_dict(device_superclass):
    """
        Generates dictionary with the class name as key and class as value. 
        Useful for constructing device class instances
    """
    constructors_by_name = {}
    for device in device_superclass.__subclasses__():
        constructors_by_name[device.__name__] = device

    return constructors_by_name

def construct_devices(data_dict, device_constructor_dict):
    """
        Returns a list constructed devices given a list of initialisation data
        Each element in devices_data_dict should be a dictionary with format 
        {
            "type": <name of device class>,
            "args": <dict of constructor args>
        }
        
        TODO: Error handling
    """
    devices = []

    # Construct device from the dictionary the device_dict above
    for device_data in data_dict:
        device_constructor = device_constructor_dict[device_data["type"]]
        device = device_constructor(**device_data["args"])

        if "name" in device_data:
            device.name = device_data["name"]

        if "default_animation" in device_data:
            ani_data = device_data["default_animation"]

            ani_type = ani_data["type"] if "type" in ani_data else ""
            args = ani_data["args"] if "args" in ani_data else {}

            device.set_animation(ani_type, **args)

        devices.append(device)

    return devices

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