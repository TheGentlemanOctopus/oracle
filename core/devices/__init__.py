import core.utilities.process_descriptor as pd
from cube_strip import CubeStrip

def construct_devices(scene_descriptor_path):
    # Load JSON
    json_data = pd.process(scene_descriptor_path)

    devices = []
    # Construct devices
    for name, data in json_data["OutputDevices"].items():
        if data["type"] == "cube_strip":
            devices.append(CubeStrip(**data["args"]))

    return devices