from CommonClient import CommonClient
import logging


class SwitchClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'switch')
        self.logger = logging.getLogger("SwitchClient")

    def setSwitchValue(self, name, value):
        if name not in self.status:
            raise RuntimeError("Unknown switch: {0}".format(name))

        self.logger.debug("Setting switch {0} to {1}".format(name, value))
        self.connector.requestAndCheck('switch', {'act': 'set', 'name': name, 'value': value})
        self.logger.debug("Switch is set successfully")
