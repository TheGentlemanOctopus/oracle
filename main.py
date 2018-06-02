#!/usr/local/bin/python
"""
    Main console app
    Combines mains from various modules by matching the first arg to a submodule main
    and passing remaining args from there
"""

import argparse
import sys
import core.sim_generator
import core.scene_manager

# Main commands
# The first argument in the app matches the key whose value is called with the remaining args
commands = {
    "sim": core.sim_generator.main,
    "scene": core.scene_manager.main
}

# Create parser
parser = argparse.ArgumentParser(
    description='THE ORACLE', 
    formatter_class=argparse.RawTextHelpFormatter,
    add_help=False,
    prefix_chars=" " # Dummy to remove help prefix
)

# Command choice
parser.add_argument("mode", 
    help="Choose your mode", 
    nargs="?", 
    default=None, 
    choices=commands.keys(), 
)

# Parse
try:
    known_args, remaining_args = parser.parse_known_args(sys.argv[1:])
except:
    parser.print_help()
    quit()

# Run command
if known_args.mode in commands:
    commands[known_args.mode](remaining_args)
else:
    parser.print_help()

