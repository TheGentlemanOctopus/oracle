from layout import Layout

import big_cube
import pixel_list

# A dictionary where key is name of layut as a string and the class as a value
layouts_by_name = {layout.__name__: layout for layout in Layout.__subclasses__()}
