import json
import sys
from core.utilities import process_descriptor 



if __name__ == '__main__':

	print sys.argv[1]

	scene_descriptor = process_descriptor.read_json(sys.argv[1])

	process_descriptor.print_element(scene_descriptor,'InputDevices')
	process_descriptor.print_element(scene_descriptor,'OutputDevices')

