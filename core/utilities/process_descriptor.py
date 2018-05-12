import json
import sys

def read_json(path):
    with open(path, 'r') as handle:
        parsed = json.load(handle)
    return parsed

def print_json(jObject):
    jstr = json.dumps(jObject, indent=4, sort_keys=True)
    print jstr
    return jstr

def process(path):
	scene_descriptor = read_json(path)
	return scene_descriptor

def print_element(d, key):
	devices = d[key]
	for k in devices.keys():
		print '\n', k
		print_json(devices[k])