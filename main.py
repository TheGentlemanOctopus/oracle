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

if __name__ == '__main__':

	print sys.argv[1]

	scene_descriptor = read_json(sys.argv[1])

	# print_json(scene_descriptor)

	input_devices = scene_descriptor['InputDevices']
	for key in input_devices.keys():
		print '\n', key
		print_json(input_devices[key])

	output_devices = scene_descriptor['OutputDevices']
	for key in output_devices.keys():
		print '\n', key
		print_json(output_devices[key])