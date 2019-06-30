# -*- coding: utf-8 -*-

import json

from AxisMixer import *
from JoystickManager import *
from Switch import *


class ControlClient:
    def __init__(self, joystickManager, servoClient, switchClient,arduinoClient, config):
        self.logger = logging.getLogger("ControlClient")
        self.joystickManager = joystickManager
        self.servoClient = servoClient
        self.switchClient = switchClient
        self.arduinoClient = arduinoClient
        self.started = False

        self.interval = float(config['interval'])
        self.configFolder = config['configFolder']

        self.Servothread = None
        self.Batterythread = None

        self.mixers = {}
        self.switches = {}
        self.joystick = None

        for name, mixerConfig in config['Mixers'].iteritems():
            mixer = AxisMixer(self, mixerConfig)
            self.mixers[name] = mixer

        for name, switchConfig in config['Switches'].iteritems():
            switch = Switch(self, switchConfig)
            self.switches[name] = switch
            switch.EvStateChanged += self.onSwitchStateChanged

    def start(self):
        if self.Servothread is not None:
            raise RuntimeError("Already started")

        self.logger.debug("Starting")
        self.Servothread = threading.Thread(target=self.threadProc)
        self.Batterythread = threading.Thread(target=self.threadBattery)
        self.Servothread.daemon = True
        self.Batterythread.daemon = True
        self.started = True
        self.Servothread.start()
        self.Batterythread.start()
        self.logger.debug("Started")

    def stop(self):
        if not self.started:
            return

        self.logger.debug("Stopping")
        self.started = False
        self.Servothread.join()
        self.Batterythread.join()
        self.Servothread = None
        self.Batterythread = None
        self.logger.debug("Stopped")

    def getAvailableJoystics(self):
        return self.joystickManager.getAvailableJoystics()

    def selectJoystick(self, joystickId):
        if self.joystick is not None:
            self.joystick.dispose()
            self.joystick = None

        self.joystick = self.joystickManager.createJoystick(joystickId)
        self.loadParams()

    def getAxes(self):
        if self.joystick is None:
            return None

        return self.joystick.getAxes()

    def getButtons(self):
        if self.joystick is None:
            return None

        return self.joystick.getButtons()

    def getMixers(self):
        return self.mixers

    def getSwitches(self):
        return self.switches

    def getParams(self):
        if self.joystick is None:
            return None

        axesParams = {}
        for axis in self.getAxes().itervalues():
            axesParams[axis.getId()] = axis.getParamsDict()

        buttonParams = {}
        for button in self.getButtons().itervalues():
            buttonParams[button.getId()] = button.getParamsDict()

        mixerParams = {}
        for name, mixer in self.getMixers().iteritems():
            mixerParams[name] = mixer.getAxesDict()

        switchParams = {}
        for name, switch in self.getSwitches().iteritems():
            switchParams[name] = switch.getButtonDict()

        return {'axesParams': axesParams, 'buttonParams': buttonParams, 'mixerParams': mixerParams,
                'switchParams': switchParams}

    def setParams(self, params):
        if self.joystick is None:
            return

        for axisId, axisParams in params.get('axesParams', {}).iteritems():
            axis = self.joystick.getAxis(int(axisId))
            if axis is not None:
                axis.setParamsDict(axisParams)

        for buttonId, buttonParams in params.get('buttonParams', {}).iteritems():
            button = self.joystick.getButton(int(buttonId))
            if button is not None:
                button.setParamsDict(buttonParams)

        for name, mixerParams in params.get('mixerParams', {}).iteritems():
            mixer = self.mixers.get(name)
            if mixer is not None:
                mixer.setAxesDict(mixerParams)

        for name, switchParams in params.get('switchParams', {}).iteritems():
            switch = self.switches.get(name)
            if switch is not None:
                switch.setButtonDict(switchParams)

    def saveParams(self):
        try:
            paramsPath = self.getParamsPath()
            if paramsPath is None:
                self.logger.warn("Cannot get params path")
                return False

            params = self.getParams()

            with open(paramsPath, 'w') as paramsFile:
                json.dump(params, paramsFile)

            return True

        except Exception, ex:
            self.logger.error(
                "{0}: Exception caught in saveParams: {1}\n{2}".format(self, ex, traceback.format_exc()).decode(
                    'utf-8'))

        return False

    def loadParams(self):
        try:
            paramsPath = self.getParamsPath()
            if paramsPath is None:
                self.logger.warn("Cannot get params path")
                return False

            params = None

            try:
                with open(paramsPath, 'r') as paramsFile:
                    params = json.load(paramsFile)
            except Exception, ex:
                self.logger.error("{0}: Exception caught while loading params from {1}: {2}\n{3}"
                        .format(self, paramsPath, ex,traceback.format_exc()).decode("utf-8"))

            if params is not None:
                self.setParams(params)
            return True

        except Exception, ex:
            self.logger.error(
                "{0}: Exception caught in loadParams: {1}\n{2}".format(self, ex, traceback.format_exc()).decode(
                    "utf-8"))

        return False

    def getParamsPath(self):
        if self.joystick is None:
            return None

        return self.configFolder + '/' + self.joystick.getName() + '.conf'

    def threadProc(self):
        while self.started:
            try:
                values = {}

                for mixer in self.mixers.itervalues():
#                    if mixer != 'engine':
                    for name, value in mixer.getServoDict().iteritems():
#                        if name != 'left_engine' and name != 'right_engine':
                        values[name] = value

                self.servoClient.setMany(values)
                time.sleep(self.interval)

            except Exception, ex:
                self.logger.error(
                    "{0}: Exception caught: {1}\n{2}".format(self, ex, traceback.format_exc()).decode("utf-8"))

    def onSwitchStateChanged(self, switch, state):
        value = 0
        if state:
            value = 1

        self.switchClient.setSwitchValue(switch.getName(), value)

    def getBatteryState(self):
        return self.arduinoClient.refreshStatus()

    def threadBattery(self):
        while self.started:
            self.getBatteryState()
            time.sleep(0.5)