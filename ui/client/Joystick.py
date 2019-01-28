from pygame import joystick

from JoystickAxis import *
from JoystickButton import *

import traceback


class Joystick:
    def __init__(self, joystickManager, id):
        self.logger = logging.getLogger("Joystick")
        self.manager = joystickManager

        self.joystick = joystick.Joystick(id)

        self.joystick.init()

        self.axes = {}
        self.buttons = {}

        for n in range(self.joystick.get_numaxes()):
            self.axes[n] = JoystickAxis(self.joystick, n)

        for n in range(self.joystick.get_numbuttons()):
            self.buttons[n] = JoystickButton(self.joystick, n)

        self.manager.EvJoystickUpdate += self.update

    def __str__(self):
        return "{0}[{1}]".format(self.getName(), self.getId())

    def getParams(self):
        axes = {}
        for id, axis in self.axes:
            axes[id] = axis.getParams()
        buttons = {}
        for id, button in self.buttons:
            buttons[id] = button.getParams()

        return {'axes': axes, 'buttons': buttons}

    def setParams(self, params):
        axes = params['axes']
        for id, params in axes:
            self.axes[id].setParams(params)

        buttons = params['buttons']
        for id, params in buttons:
            self.buttons[id].setParams(params)

    def getName(self):
        return self.joystick.get_name().strip();

    def getId(self):
        return self.joystick.get_id();

    def getAxesNumber(self):
        return len(self.axes)

    def getAxes(self):
        return self.axes.copy()

    def getButtonsNumber(self):
        return len(self.buttons)

    def getButtons(self):
        return self.buttons.copy()

    def getAxis(self, n):
        return self.axes.get(n, None)

    def getButton(self, n):
        return self.buttons.get(n, None)

    def update(self):
        try:
            if not self.joystick.get_init():
                return

            for axis in self.axes.itervalues():
                axis.update()

            for button in self.buttons.itervalues():
                button.update()

        except Exception, ex:
            self.logger.error("{0}: Exception caught in update: {1}\n{2}".format(self, ex, traceback.format_exc()))

    def dispose(self):
        self.manager.EvJoystickUpdate -= self.update

        if self.joystick.get_init():
            self.joystick.quit()
            self.joystick = None
            self.axes = {}
            self.buttons = {}
