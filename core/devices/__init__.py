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
    # Construct devices
    for device_json in json_data["OutputDevices"]:
        devices.append(device_dict[device_json["type"]](**device_json["args"]))

    return devices