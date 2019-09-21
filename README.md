# The Oracle

Generate sound reactive patterns for the Oracle art installation. Based on a generalised 'art scene' model, the framework provided here is extendable for future interactive led art installations. During runtime, output rgb data is sent over UDP using [OpenPixelControl (OPC)](https://github.com/zestyping/openpixelcontrol)

## Installation

To use the oracle, you'll need to install a couples pieces of software on your mac/linux development machine. 

* Install python packages with

`$ pip install -r requirements.txt`

* Led displays are simulated with [OPC's gl_server](https://github.com/zestyping/openpixelcontrol). After installation, ensure `gl_server` is reachable on the path, e.g.

`$ sudo ln -s PATH_TO_GL_SERVER /usr/local/bin/gl_server`

## Scenes

A scene describes the various interacting components of an art installation.
Scenes are defined in a scene file encoded in JSON format. 
Example scenes can be found under `descriptors/` 

### Running a scene

To begin pattern generation, run a scene by calling

`$ python main.py scene PATH_TO_SCENE_FILE`

This requires the receiving OPC server to be running at the address defined in `SceneDetails`.

### Simulate a scene

For those wishing to develop patterns that don't have access to hardware, you can simulate scenes with

`$ python main.py sim PATH_TO_SCENE`

This launches an instance of `gl_server` with the appropriate led cloud. Following that, in a separate prompt, launch the scene as normal to begin pattern generation (as above) 

| ![Alt text](/docs/simulator.png?raw=true "/descriptors/PointCloudScene.json") |
(/descriptors/PointCloudScene.json)

### File structure

A scene file requires three top-level keys
* `SceneDetails` - opc communication settings and framerate
* `InputDevices` - An array of input devices, e.g. fft data streamed over udp
* `OutputDevices` - An array of output devices, e.g. the Oracle

All devices must contain a `type` key indicating the type of device. Output devices must also specify a `name` key for reference. 

For example, consider the scene file 
```
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
            "name": "BigDaddy",
            "type": "BigCubeDevice",
            "args": {
                "channel": 1,
                "led_spacing" : 0.2,
                "strip_spacing": 0.05
            },
            "default_animation": {
                "type": "SwoopyTown",
                "args": {}
            }
        }
    ]
}
```

This scene contains one input device, a pattern controller app, and one output device, a BigCubeDevice led display.

## Devices

Devices are individual components that either generate stimulus affecting pattern generation (input device) or generate rgb data send over opc (output device). In scene files, each device must contain a `type` (indicating device class) and an `args` object that defines initialisation data.

### Input Devices

The `AppDevice` is a http app (Flask) for controlling high level pattern parameters.
Args
* `host` - str - App IP
* `port` - int - App Port



