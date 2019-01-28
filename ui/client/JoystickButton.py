import logging
from Joystick import *
import traceback
from python_modules.common_utils import MulticastDelegate

class JoystickButton:
    def __init__(self, joystick, buttonId):
        self.logger = logging.getLogger("JoystickButton")

        self.joystick = joystick
        self.id = buttonId

        self.toggle = False

        self.EvStateChange = MulticastDelegate()

        self.pushed = False

        self.pressed = False

    def setParams(self, toggle):
        self.toggle = toggle

    def setParamsDict(self, params):
        self.setParams(bool(params['toggle']))

    def getParams(self):
        return (self.toggle)

    def getParamsDict(self):
        return {'toggle': self.toggle}

    def getId(self):
        return self.id

    def getState(self):
        return self.pushed

    def getName(self):
        return "Button {0}".format(self.getId())

    def update(self):
        if not self.joystick.get_init():
            return

        oldValue = self.pushed
        newValue = self.convert(self.joystick.get_button(self.id))
        self.pushed = newValue

        if oldValue != newValue:
            self.EvStateChange(self, self.pushed)

    def convert(self, value):
        if not self.toggle:
            return value

        oldValue = self.pressed
        self.pressed = value

        if oldValue and not value:
            return not self.pushed

        return self.pushed
