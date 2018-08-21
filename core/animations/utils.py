from animation import Animation

def animations_by_layout():
    """
        A dictionary where
           key: name of the layout class as a string
           value: dictionary of animations keyed by name
    """
    animations_by_layout = {}
    for animation in Animation.__subclasses__():
        if animation.layout_type in animations_by_layout:
            animations_by_layout[animation.layout_type][animation.__name__] = animation

        else:
            animations_by_layout[animation.layout_type] = {animation.__name__: animation}

    return animations_by_layout

def possible_animations(name):
    """
        returns a dict of possible animations that include:
           - generic Layout type
           - layout specific types
    """
    animation_dict = animations_by_layout()

    possible_animations = {}
    if "Layout" in animation_dict:
        possible_animations.update(animation_dict["Layout"])

    if name in animation_dict:
        possible_animations.update(animation_dict[name])

    return possible_animations


def add_params(animation, params, **kwargs):
    """
        Adds a dictioanry of parameters and overrides to an animation
    """
    # Sort out params
    for name, value in kwargs.items():
        if not name in params:
            raise Exception("Unknonwn params: %s"%name)

        params[name][0] = value
    
    for name, value in params.items():
        animation.add_param(name, value[0], value[1], value[2])