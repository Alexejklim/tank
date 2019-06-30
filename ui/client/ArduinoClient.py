# -*- coding: utf-8 -*-

import logging
from CommonClient import CommonClient
from python_modules.common_utils import MulticastDelegate

__all__ = ['ArduinoClient']

class ArduinoClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'arduino')
        host, port = addr
        self.host = host
        self.logger = logging.getLogger("ArduinoClient")
        self.EvBatteryMove = MulticastDelegate()
        self.battery = {'charge': 0, 'voltage': 0.0,'current': 0.0}


    def refreshStatus(self):
        self.logger.debug("Getting status")
        result = self.connector.requestAndCheck(self.request, {'act': 'status'})
        self.status = result.get('battery').get('status')
        if self.status == 'OK':
            self.setBattery(result)
            self.EvBatteryMove()
            self.logger.debug("Status is got successfully")

    def setBattery(self,result):
        self.battery['voltage'] = result.get('battery').get('Voltage')
        self.battery['current'] = result.get('battery').get('Current')
        self.battery['charge'] = int((self.battery['current']-4)*10)