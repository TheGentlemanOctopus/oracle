# The Oracle

Generate sound reactive animations for the Oracle art installation. Based on a generalised 'art scene' model, the framework provided here is extendable for future interactive led art installations. During runtime, output rgb data is communicated over UDP using the [OpenPixelControl (OPC)](https://github.com/zestyping/openpixelcontrol) protocol.

## Installation

To use the oracle, you'll need to install a couple pieces of software on your mac/linux development machine. 

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

For those wishing to develop animations that don't have access to hardware, you can simulate scenes with

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

Devices are individual components that either generate stimulus affecting pattern generation (input device) or generate rgb data send over opc (output device). In scene files, each device must contain a `type` (indicating device class) and an `args` object that defines initialisation data. Each device runs as a serparate python process (via multiprocessing API) so processing can be split across multiple cores. 

### AppDevice (InputDevice)

The `AppDevice` is a http app (Flask) for switching of patterns and control high level pattern parameters.
A drop-down menu provides a list of compatible patterns for the current scene. 
For real-time configuration, sliders are provided for each parameter of the currently selected pattern.

![Alt text](/docs/app.png?raw=true "/descriptors/PointCloudScene.json")

### FftDevice (InputDevice)

The `FftDevice` receives 7-band fft data (0-127) over serial. Data should be formatted by a comma separated string terminated by newline, eg. `30,78,0,0,127,68,127\n`. Sends a start message during initialisation.

### OutputDevices

An `OutputDevice` is an led display. Each output device in a scene file must contain a `name` key as a reference. Optionally, a `default_animation` key can be defined to indicate  which pattern should run at startup (useful for production), see the example scene above. For flexible opc connectivity, each `OutputDevice` can output across multiple opc channels.
The `layout_type` property defined on the class defines the type of animations that are compatible (and thus selectable via the app)

Example `OutputDevices` include
* `Lonely` - The simplest led display, a singular pixel
* `BigCubeDevice` - A cube of led strips
* `PointCloudDevice` - A generic point cloud of pixels, defined in json under `core/point_clouds/`

## Animations

`Animation` classes are used to define sound reactive animations. Although an animation can work across multiple output devices, it's `layout_type` parameter must be compatible. To make an animation, subclass `Animation` in a new module and store it under `core/animations/`. Import the new module under `core/animation/__init__.py` to make it accessible to `main.py`.
Each animation defines a number of `Param`'s, that define the sliders that appear on the app. 

Notable examples (found in `core/animations/`)
* `Carousel` - cycles between different animations
* `SpiralOutFast` - sonic travelling waves
* `FireGlow` - warm, firey goodness
* `LavaLamp` - squelchy, bloby, drifty

## Layouts

A `Layout` abstracts an arrangement of pixels. Each `Animation` is associated with a specific layout class, via the `layout_type` property, indicating which layout it is compatible with. Similarly, an `OutputDevice` defines the mapping of layout pixels to opc channels and defines a similar `layout_type` property. A `Layout` can itself be composed of `Layout`s, allowing complex structures to be defined.

Current layouts include:
* `pixel_list` - a generic list of pixels (eg for point clouds)
* `strip` - a linear strip of leds
* `big_cube` - strips of leds arranged in a cube
