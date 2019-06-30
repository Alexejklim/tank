import logging
import time
import traceback

from python_modules.command_utils.serial_client_connector import SerialClientConnector


class ArduinoController:
    def __init__(self, config):
        self.logger = logging.getLogger("ArduinoController")
        self.port = config['port']
        self.speed = config['speed']
        self.timeout = config['timeout']
        self.connector = None

    def start(self):
        if self.connector is not None:
            raise RuntimeError("Arduino controller already started")

        self.logger.info("Starting")
        self.connector = SerialClientConnector(self.port, self.speed, self.timeout)
        self.logger.info("Started")

    def stop(self):
        if self.connector is None:
            return

        self.logger.info("Stopping")
        self.connector.dispose()
        self.connector = None;
        self.logger.info("Stopped")

    def getBateryStatus(self):
        return self.connector.requestAndCheck('battery', {'act': 'status'})

    def getStatus(self):
        return {'battery': self.getBateryStatus()}

class arduinoCommandHandler:
    def __init__(self, ArduinoController):
        self.ArduinoController = ArduinoController

    def handleCommand(self, cmd, args):
        if cmd != 'arduino':
            raise NotImplementedError("Wrong command: {0}".format(cmd))

        action = args.get('act')

        if action == 'status':
            return self.ArduinoController.getStatus()

        elif action == 'start':
            self.ArduinoController.start()
            return True
        elif action == 'stop':
            self.ArduinoController.stop()
            return True
        else:
            raise NotImplementedError("Wrong action: {0}".format(action))