import json

from os.path import join, dirname, abspath, isfile
from core.devices.pixel import Pixel

"""
    This module contains point clouds that can be used to construct PointCloud devices
    point cloud files should be json files in the same format as gl_server, eg
    [
        {"point": [1,0,0]},
        {"point": [0,1,0]}
    ]
"""

# Module path
path = join(dirname(abspath(__file__)), "")

def load_point_cloud(filename):
    filepath = path + filename

    # Check file exists
    if not isfile(filepath):
        raise Exception("Cannot find point cloud file "+filepath)

    # Load data as json
    with open(filepath) as f:
        data = json.load(f)

    # Construct pixels
    return [Pixel(i["point"]) for i in data]
