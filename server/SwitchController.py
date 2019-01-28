import logging


class SwitchController:
    def __init__(self, config):
        self.logger = logging.getLogger("SwitchController")
        self.switches = {}

    def addAll(self, names, setFunction, getFunction, type=None):
        for name in names:
            self.addSwitch(name, setFunction, getFunction, type)

    def addSwitch(self, name, setFunction, getFunction, type=None):
        if name in self.switches:
            raise RuntimeError("Switch {0} already exists".format(name))

        self.switches[name] = {'set': setFunction, 'get': getFunction, 'type': type}

    def delSwitch(self, name):
        if name not in self.switches:
            raise RuntimeError("Wrong switch name: {0}".format(name))

        self.switches.pop(name)

    def setSwitchValue(self, name, value):
        if name not in self.switches:
            raise RuntimeError("Wrong switch name: {0}".format(name))

        switch = self.switches.get(name)
        switch['set'](name, value)

    def getSwitchValue(self, name):
        if name not in self.switches:
            raise RuntimeError("Wrong switch name: {0}".format(name))

        switch = self.switches.get(name)
        value = switch['get'](name)

        return value

    def start(self):
        self.logger.info("Starting")
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.clearSwitches()
        self.logger.info("Stopped")

    def clearSwitches(self):
        self.logger.info("Clearing switches")
        self.switches.clear()

    def getStatus(self):
        switchStatus = {}

        for name in self.switches.iterkeys():
            switch = self.switches[name]
            switchStatus[name] = {'type': switch['type'], 'value': self.getSwitchValue(name)}

        return switchStatus


class SwitchCommandHandler:
    def __init__(self, switchController):
        self.switchController = switchController

    def handleCommand(self, cmd, args):
        if cmd != 'switch':
            raise NotImplementedError("Wrong command: {0}".format(cmd))

        action = args.get('act')

        if action == 'set':
            name = args.get('name')
            value = args.get('value')
            self.switchController.setSwitchValue(name, value)

            if args.get('_protocol', '') == 'udp':
                return {'_noAnswer': True}

            return True

        elif action == 'get':
            name = args.get('name')
            value = self.switchController.getSwitchValue(name)
            return {'switchName': name, 'switchValue': value}

        elif action == 'status':
            return {'switchStatus': self.switchController.getStatus()}

        elif action == 'start':
            self.switchController.start()
            return True
        elif action == 'stop':
            self.switchController.stop()
            return True

        else:
            raise NotImplementedError("Wrong action: {0}".format(action))
