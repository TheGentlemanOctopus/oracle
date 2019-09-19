# The Oracle

This repo contains code to drive sound reactive patterns for the Oracle art installation. The framework provided here was designed to be easily extendable to allow future sound-reactive led art installations to be designed and made. Built using openpixelcontrol.

## Installation

To use the oracle, you'll need a couple bits of software. 
Install required python packages with 
`pip install -r requirements.txt`

For simulation of led displays we use [openpixelcontrol's gl_server](https://github.com/zestyping/openpixelcontrol). After installation, ensure it is reachable on the path, e.g.
`sudo ln -s PATH_TO_GL_SERVER` /usr/local/bin/gl_server

To run:

$ python main.py mode=sim descriptors/WonderFace.json
