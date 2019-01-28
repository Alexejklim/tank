from CommonClient import CommonClient
import logging


class TankClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'tank')
        self.logger = logging.getLogger("TankClient")

    def reset(self):
        self.logger.debug("Resetting tank")
        self.connector.requestAndCheck('tank', {'act': 'reset'})
        self.logger.debug("Tank reset is successful")
