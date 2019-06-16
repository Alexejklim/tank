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

        self.initRequests = config['Init']
        self.deinitRequests = config['Deinit']

        self.connector = None

    def start(self):
        if self.connector is not None:
            raise RuntimeError("Arduino controller already started")

        self.logger.info("Starting")
        self.connector = SerialClientConnector(self.port, self.speed, self.timeout)

        self.logger.info("Sending inittial requests")
        while True:
            try:
                for request in self.initRequests:
                    self.logger.info("Sending initial request {0}".format(request))
                    self.connector.requestAndCheck(request['cmd'], request['args'])
                break
            except Exception, ex:
                self.logger.error("{0}: Exception caught: {1}\n{2}".format(self, ex, traceback.format_exc()))
                time.sleep(1)

        self.logger.info("Started")

    def stop(self):
        if self.connector is None:
            return

        self.logger.info("Stopping")

        for request in self.deinitRequests:
            self.logger.info("Sending final request {0}".format(request))
            self.connector.requestAndCheck(request['cmd'], request['args'])

        self.connector.dispose()
        self.connector = None;
        self.logger.info("Stopped")

    def getBateryStatus(self):
        return self.connector.requestAndCheck('battery', {'act': 'status'})

    def setGunPower(self, name, value):
        self.connector.requestAndCheck('gun', {'act': 'power', 'value': value})

    def getGunStatus(self):
        return self.connector.requestAndCheck('gun', {'act': 'status'})

    def getGunPower(self, name):
        return self.getGunStatus()['power'];

    def setGunFire(self, name, value):
        if value == "1":
            self.connector.requestAndCheck('gun', {'act': 'fire'})

    def getGunFire(self, name):
        return 0

    def getStatus(self):
        return {'battery': self.getBateryStatus(), 'gun': self.getGunStatus()}
