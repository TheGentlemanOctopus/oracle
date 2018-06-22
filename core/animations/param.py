class Param(object):
    """
        A parameter is a value affecting a pattern that doesn't change very often
        The param value is limited to its extents during setting
    """
    def __init__(self, value, minimum, maximum):
        self._value = value
        self.min = minimum
        self.max = maximum

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, x):
        if x < self.min:
            self._value = self.min

        elif x > self.max:
            self._value = self.max

        else:
            self._value = x