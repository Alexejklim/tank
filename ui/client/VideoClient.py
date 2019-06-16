# -*- coding: utf-8 -*-

import logging
from CommonClient import CommonClient

__all__ = ['VideoClient']

class VideoClient(CommonClient):
    def __init__(self, addr):
        CommonClient.__init__(self, addr, 'video')
        host, port = addr
        self.host = host
        self.logger = logging.getLogger("VideoClient")
        self.devices = {}
        self.captures = {}

    def refreshStatus(self):
        CommonClient.refreshStatus(self)
        self.devices = self.status['devices']

    def getDevices(self):
        return self.devices

    def startCapture(self, name, width, height, bitrate, fps, host):
        if name not in self.devices:
            raise RuntimeError("Invalid name: {0}".format(name))

        if name in self.captures:
            raise RuntimeError("Capture already started at {0}".format(name))

        self.logger.debug("Starting capture at {0}".format(name))
        result = self.connector.requestAndCheck('video',
                                                {'act': 'startCapture', 'name': name, 'width': width, 'height': height,
                                                 'bitrate': bitrate, 'fps': fps, 'host': host})
        self.captures[name] = name
        return result['port']

    def stopCapture(self, name):
        if name not in self.captures:
            return RuntimeError("Invalid name: {0}".format(name))

        self.logger.debug("Stopping capture at {0}".format(name))
        self.captures.pop(name)
        self.connector.requestAndCheck('video', {'act': 'stopCapture', 'name': name})
        self.logger.debug("Capture stopped at {0}".format(name))

    def stopAllCaptures(self):
        self.logger.debug("Stopping all captures")
        for name in self.captures.keys():
            self.stopCapture(name)

    def stop(self):
        self.logger.debug("Stopping")
        self.stopAllCaptures()
        CommonClient.stop(self)
        self.logger.debug("Stopped")
