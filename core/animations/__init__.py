from animation import Animation

# Import animations here to make them detectable to higher level code
import big_cube_walk
import swoopy_town

# A dictionary where
#    key: name of the layout class as a string
#    value: dictionary of animations keyed by name
animations_by_layout = {}
for animation in Animation.__subclasses__():
    if animation.layout_type in animations_by_layout:
        animations_by_layout[animation.layout_type][animation.__name__] = animation

    else:
        animations_by_layout[animation.layout_type] = {animation.__name__: animation}

def possible_animations(name):
    """
        returns a dict of possible animations that include:
           - generic Layout type
           - layout specific types
    """
    possible_animations = {}
    if "Layout" in animations_by_layout:
        possible_animations.update(animations_by_layout["Layout"])

    if name in animations_by_layout:
        possible_animations.update(animations_by_layout[name])

    return possible_animations


