# -*- coding: utf-8 -*-

import logging

from python_modules.command_utils import HttpClientConnector


class CommonClient:
    def __init__(self, addr, request):
        self.logger = logging.getLogger("CommonClient[{0}]".format(request))
        self.addr = addr
        self.request = request
        self.statusKey = request + "Status"
        self.status = {}
        
    def refreshStatus(self):
        self.logger.debug("Getting status")
        result = self.connector.requestAndCheck(self.request, {'act': 'status'})
        
        self.status = result[self.statusKey];
        self.logger.debug("Status is got successfully")

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status
        
    def start(self):
        self.logger.debug("Starting common")
        self.connector = HttpClientConnector(self.addr)
        self.refreshStatus()
        self.logger.debug("Started common")

    def stop(self):
        self.logger.debug("Stopping common")
        if self.connector is not None:
            self.connector.dispose()
            self.connector = None

        self.status = {}
        self.logger.debug("Stopped common")
        