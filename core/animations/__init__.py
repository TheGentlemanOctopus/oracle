from animation import Animation

import big_cube_walk

# A dictionary where the key is the layout class the animation requires
# and the value is the layout
animations_by_layout = {}
for animation in Animation.__subclasses__():
    if animation.layout_type in animations_by_layout:
        animations_by_layout[animation.layout_type][animation.__name__] = animation

    else:
        animations_by_layout[animation.layout_type] = {animation.__name__: animation}