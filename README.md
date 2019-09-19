# The Oracle

This repo contains code to generate sound reactive patterns for the Oracle art installation. The framework provided here was designed to be extendable for future sound-reactive led art installations. Led rgb data is communicated over UDP using [OpenPixelControl (OPC)](https://github.com/zestyping/openpixelcontrol)

## Installation

To use the oracle, you'll need a couple bits of software. 
First, install required python packages with

`$ pip install -r requirements.txt`

For simulation of led displays we use [openpixelcontrol's (OPCs) gl_server](https://github.com/zestyping/openpixelcontrol). After installation, ensure it is reachable on the path, e.g.

`$ sudo ln -s PATH_TO_GL_SERVER /usr/local/bin/gl_server`

## Scenes

A scene describes the various interacting components of an art installation.
Scenes are defined in a scene file encoded in JSON format. 
Example scenes can be found under `descriptors/` 

### Running a scene

To run a scene call

`$ python scene PATH_TO_SCENE_FILE`

This requires the receiving OPC server to be running at the address defined in `SceneDetails`

### Simulate a scene

For those wishing to develop patterns that don't have access to hardware, you can simulate scenes with the opc gl_server. 

`$ python main.py sim PATH_TO_SCENE`

### File structure

Each scene file should contain three top-level keys
* `SceneDetails` - opc communication settings and framerate
* `InputDevices` - An array of input devices (see below). E.g. fft data streamed over udp
* `OutputDevices` - An array of output devices (see below). E.g. the Oracle

For example, here is a minimal scene file 

{
    "SceneDetails": {
        "scene_fps" : 60,
        "device_fps": 30,
        "opc_host": "127.0.0.1",
        "opc_port": 7890,
        "r_scaling": 0.5,
        "g_scaling": 0.5,
        "b_scaling": 0.5
    },
    "InputDevices": [
        {
            "type": "AppDevice",
            "args": {
                "host": "127.0.0.1",
                "port": 5000
            }
        }
    ],
    "OutputDevices": [
        {
            "name": "Cloudface",
            "type": "PointCloudDevice",
            "args": {
                "channel": 1,
                "pixels": "face.json"
            }
        }
    ]
}


