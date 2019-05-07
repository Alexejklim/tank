# -*- coding: utf-8 -*-

import socket
import logging

from .client_connector import ClientConnector


class UdpClientConnector(ClientConnector):
    def __init__(self, addr):
        ClientConnector.__init__(self)
        self.logger = logging.getLogger("UdpClientConnector")

        self.addr = addr

        self.logger.debug("Binding UDP socket")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", 0))

        self.logger.debug("UDP socket bound to {0}".format(self.socket.getsockname()))

    def _doRequest(self, requestString):
        if self.socket is None:
            raise RuntimeError("Connector is disposed")

        self.logger.debug("Sending {0} to {1}".format(requestString, self.addr))
        self.socket.sendto(requestString, self.addr)

    def dispose(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
