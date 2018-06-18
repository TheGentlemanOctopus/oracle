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