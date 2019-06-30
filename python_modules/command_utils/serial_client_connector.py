# -*- coding: utf-8 -*-

import threading
import serial
import json
import logging
import time

from .client_connector import ClientConnector


class SerialClientConnector(ClientConnector):
    def __init__(self, port, speed, timeout, initial_timeout=0.0):
        ClientConnector.__init__(self)
        self.logger = logging.getLogger("SerialPortClientConnector")

        self.port = port
        self.speed = speed
        self.timeout = timeout

        self.lock = threading.Lock()

        self.logger.debug("Opening {0} at speed {1} with timeout {2}".format(self.port, self.speed, self.timeout))
        self.serialPort = serial.Serial(self.port, self.speed, timeout=self.timeout)

        self.logger.debug("Waiting initial sleep {0}".format(initial_timeout))
        time.sleep(initial_timeout)
        self.logger.debug("{0} opened".format(self.port))

    def _doRequest(self, requestString):
        if self.serialPort is None:
            raise RuntimeError("Connector is disposed")

        with self.lock:
            self.logger.debug("Sending {0} to {1}".format(requestString, self.port))
            self.serialPort.write(requestString+'\n')
            self.logger.debug("Receiving answer from {0}".format(self.port))
            data = self.serialPort.read(20480)
        self.logger.debug("Response body is {0}".format(data))
        result = json.loads(data)
        self.logger.debug("Parsed result is {0}".format(result))
        return result

    def dispose(self):
        if self.serialPort is not None:
            self.serialPort.close()
            self.serialPort = None
            self.lock = None
