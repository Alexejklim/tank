import logging
from Joystick import *
import traceback

from python_modules.common_utils import MulticastDelegate


class JoystickAxis:
    def __init__(self, joystick, axisId, axisThreshold=0.01):
        self.logger = logging.getLogger("JoystickAxis")

        self.joystick = joystick
        self.axisId = axisId

        self.axisThreshold = axisThreshold

        self.gamma = 1.0
        self.trim = 0.0
        self.invert = False

        self.EvAxisMove = MulticastDelegate()

        self.value = 0
        self.inputValue = 0

    def setParams(self, gamma, trim, invert):
        self.gamma = gamma
        self.trim = trim
        self.invert = invert

    def getParams(self):
        return self.gamma, self.trim, self.invert

    def setParamsDict(self, params):
        self.setParams(float(params['gamma']), float(params['trim']), bool(params['invert']))

    def getParamsDict(self):
        return {'gamma': self.gamma, 'trim': self.trim, 'invert': self.invert}

    def getId(self):
        return self.axisId

    def getName(self):
        return "Axis {0}".format(self.getId())

    def getValue(self):
        return self.value

    def getInputValue(self):
        return self.inputValue

    def update(self):
        if not self.joystick.get_init():
            return

        oldValue = self.value
        oldInputValue = self.inputValue

        newInputValue = self.joystick.get_axis(self.axisId)
        newValue = self.convert(newInputValue)

        self.value = newValue
        self.inputValue = newInputValue

        if (abs(newValue - oldValue) >= self.axisThreshold) or (
            abs(newInputValue - oldInputValue) >= self.axisThreshold):
            self.EvAxisMove(self, newValue, newInputValue)

    def convert(self, value):
        negative = value < 0.0

        value = pow(abs(value), self.gamma)

        if (negative and not self.invert) or (not negative and self.invert):
            value = -value

        value += self.trim

        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        return value
