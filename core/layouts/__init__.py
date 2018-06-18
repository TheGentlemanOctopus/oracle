from layout import Layout

import big_cube

# A dictionary where key is name of layut as a string and the class as a value
layouts_by_name = {layout.__name__: layout for layout in Layout.__subclasses__()}
layouts_by_name["Layout"] = Layout