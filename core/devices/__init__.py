import core.utilities.process_descriptor as pd
from device import Device

# To be able construct a device, all you have to is import it here 
import cube_strip
import lonely

classes = Device.__subclasses__()
device_dict = {}
for device in classes:
    device_dict[device.__name__] = device


def construct_devices(scene_descriptor_path):
    # Load JSON
    json_data = pd.process(scene_descriptor_path)

    devices = []
    # Construct devices
    for name, data in json_data["OutputDevices"].items():
        devices.append(device_dict[data["type"]](**data["args"]))

    return devices