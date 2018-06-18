from layout import Layout

import big_cube

# A dictionary where:
#     key: name of layout as a string
#     value: layout class/subclass
layouts_by_name = {layout.__name__: layout for layout in Layout.__subclasses__()}
layouts_by_name["Layout"] = Layout