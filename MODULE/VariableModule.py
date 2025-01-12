from typing import Optional
from MODULE.SystemModule import SYSTEM

class IntegerVariable:
    def __init__(
        self, data: int = 0, min: Optional[int] = None, max: Optional[int] = None
    ):
        self.__data = data
        if self.__data is None:
            self.isValid = False
        else:
            self.isValid = True
        self.__max = max
        self.__min = min

    @property
    def current(self):
        return self.__data

    @property
    def max(self):
        return self.__max

    @property
    def min(self):
        return self.__min

    def adjust(self):
        if self.__max is not None and self.__data > self.__max:
            self.__data = self.__max
        if self.__min is not None and self.__data < self.__min:
            self.__data = self.__min

    def checkType(self, other):
        if not isinstance(other, int):
            raise TypeError("Only Integer Granted")

    def __add__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return self.__data + other

    def __radd__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return other + self.__data

    def __sub__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return self.__data - other

    def __rsub__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return other - self.__data

    def __mul__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return self.__data * other

    def __rmul__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return other * self.__data

    def __truediv__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            return int(self.__data / other)

    def __rtruediv__(self, other):
        if self.__data is None:
            return other
        else:
            self.checkType(other)
            return int(other / self.__data)

    def __iadd__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data += other
            self.adjust()
            return self

    def __isub__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data -= other
            self.adjust()
            return self

    def __imul__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data *= other
            self.adjust()
            return self

    def __itruediv__(self, other):
        if self.__data is None:
            return self
        else:
            self.checkType(other)
            self.__data = int(self.__data / other)
            self.adjust()
            return self

    def set(self, other):
        self.__data = other
        self.adjust()

    def setMax(self, other):
        self.__max = other

    def setMin(self, other):
        self.__min = other


class InvertedVariable:
    def __init__(self, name: list[str], value=0):
        self.__name = tuple(name)
        self.isValid = True
        self.data = IntegerVariable(value)

    @property
    def name(self):
        if self.data.current > 0:
            return SYSTEM.fstr(self.__name[0], 2)
        elif self.data.current < 0:
            return SYSTEM.fstr(self.__name[1], 2)
        else:
            return SYSTEM.fstr("--", 2)


class TagedVariable:
    def __init__(self, name: str, minValue=None, maxValue=None, isValid=True, value=0):
        self.__name = name
        self.isValid = isValid
        if self.isValid:
            self.data = IntegerVariable(value, minValue, maxValue)
        else:
            self.data = IntegerVariable(None)

    @property
    def name(self):
        return SYSTEM.fstr(self.__name, 3)
