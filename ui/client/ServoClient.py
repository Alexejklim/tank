from CommonClient import *

import logging
import string

from python_modules.command_utils import UdpClientConnector


class ServoClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'servo')
        self.logger = logging.getLogger("ServoClient")

    def setServoValue(self, name, value):
        if name not in self.status:
            raise RuntimeError("Unknown servo: {0}".format(name))

        self.logger.debug("Setting servo {0} to {1}".format(name, value))
        self.udpConnector.request('servo', {'act': 'set', 'name': name, 'value': value})
        self.logger.debug("Servo is set successfully")

    def setMany(self, servos):
        values = [];

        for name, value in servos.iteritems():
            if name not in self.status:
                raise RuntimeError("Unknown servo: {0}".format(name))
            values.append("{0}:{1}".format(name, value))

        if len(values) > 0:
            self.udpConnector.request('servo', {'act': 'setmany', 'values': string.join(values, ',')})

    def start(self):
        self.logger.debug("Starting")
        self.udpConnector = UdpClientConnector(self.addr)
        CommonClient.start(self)
        self.logger.debug("Started")

    def stop(self):
        self.logger.debug("Stopping")

        if self.udpConnector is not None:
            self.udpConnector.dispose()
            self.udpConnector = None

        CommonClient.stop(self)
        self.logger.debug("Stopped")
