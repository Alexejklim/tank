from CommonClient import CommonClient
import logging


class GpioClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'gpio')
        self.logger = logging.getLogger("GpioClient")

    def setGpioValue(self, name, value):
        if name not in self.status:
            raise RuntimeError("Unknown gpio: {0}".format(name))

        self.logger.debug("Setting gpio {0} to {1}".format(name, value))
        self.connector.requestAndCheck('gpio', {'act': 'set', 'name': name, 'value': value})
        self.logger.debug("Gpio is set successfully")
