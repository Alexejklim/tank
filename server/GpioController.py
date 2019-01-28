import logging
import os


class GpioController:
    # BASEPATH = "/sys/class/gpio"

    def __init__(self, config):
        self.logger = logging.getLogger("GpioController")
        self.pins = {}
        self.basePath = config['basePath']
        self.pinConfig = config['Pins']

    def start(self):
        if len(self.pins) > 0:
            raise RuntimeError("Gpio controller already started")

        self.logger.info("Starting")
        for (name, value) in self.pinConfig.iteritems():
            self.addPin(name, value['pin'], value['dir'])

        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.releaseAll()
        self.logger.info("Stopped")

    def addPin(self, name, pinNumber, pinDirection):
        self.logger.info("Adding pin {0} with number {1} and direction {2}".format(name, pinNumber, pinDirection))

        pin = {'pin': pinNumber, 'dir': pinDirection, 'path': "{0}/gpio{1}".format(self.basePath, pinNumber)}
        self.exportPin(pin)
        self.pins[name] = pin

    def setPinValue(self, name, value):
        if name not in self.pins:
            raise IndexError("Wrong pin name: {0}".format(name))

        pin = self.pins.get(name)
        if pin['dir'] != 'out':
            raise IOError("Wrong pin direction: {0}".format(pin['dir']))

        with open(pin['path'] + "/value", "w") as f:
            f.write("{0}\n".format(value))

    def getPinValue(self, name):
        if name not in self.pins:
            raise IndexError("Wrong pin name: {0}".format(name))

        pin = self.pins.get(name)

        with open(pin['path'] + "/value", "r") as f:
            value = int(f.readline())

        return value

    def getStatus(self):
        pinStatus = {}

        for name in self.pins.iterkeys():
            pinStatus[name] = self.pins[name].copy()
            pinStatus[name]['value'] = self.getPinValue(name)

        return pinStatus

    def getPinNames(self):
        return self.pins.keys()

    def releasePin(self, name):
        if name not in self.pins:
            raise IndexError("Wrong pin name: {0}".format(name))

        self.logger.info("Releasing pin {0}".format(name))

        pin = self.pins.pop(name)
        self.unexportPin(pin)

    def releaseAll(self):
        self.logger.info("Releasing all pins")

        for pin in self.pins.itervalues():
            self.unexportPin(pin)

        self.pins.clear()

    def exportPin(self, pin):
        if not os.path.isdir(pin['path']):
            with open(self.basePath + "/export", "w") as f:
                f.write("{0}\n".format(pin['pin']))

            if not os.path.isdir(pin['path']):
                raise RuntimeError("Cannot export GPIO pin {0}".format(pin['pin']))

        f = open(pin['path'] + "/direction", "w")
        f.write(pin['dir'])
        f.close()

    def unexportPin(self, pin):
        with open(self.basePath + "/unexport", "w") as f:
            f.write("{0}\n".format(pin['pin']))


class GpioCommandHandler:
    def __init__(self, gpioController):
        self.gpioController = gpioController

    def handleCommand(self, cmd, args):
        if cmd != 'gpio':
            raise NotImplementedError("Wrong command: {0}".format(cmd))

        action = args.get('act')

        if action == 'set':
            name = args.get('name')
            value = args.get('value')
            self.gpioController.setPinValue(name, value)

            if args.get('_protocol', '') == 'udp':
                return {'_noAnswer': True}

            return True

        elif action == 'get':
            name = args.get('name')
            value = self.gpioController.getPinValue(name)
            return {'gpioName': name, 'gpioValue': value}

        elif action == 'status':
            return {'gpioStatus': self.gpioController.getStatus()}

        elif action == 'start':
            self.gpioController.start()
            return True
        elif action == 'stop':
            self.gpioController.stop()
            return True

        else:
            raise NotImplementedError("Wrong action: {0}".format(action))
