# -*- coding: utf-8 -*-

import json
import logging
import httplib

from ..cross_version import http_client
from .client_connector import ClientConnector


class HttpClientConnector(ClientConnector):
    def __init__(self, addr):
        ClientConnector.__init__(self)
        self.logger = logging.getLogger("HttpClientConnector")

        host, port = addr
        self.addr = "{0}:{1}".format(host, port)

    def _doRequest(self, requestString):
        self.logger.debug("Sending {0} to {1}".format(requestString, self.addr))

        conn = httplib.HTTPConnection(self.addr)
        try:
            conn.request("GET", requestString)
            resp = conn.getresponse()

            self.logger.debug("Response is {0} {1}".format(resp.status, resp.reason))

            if resp.status != 200:
                raise RuntimeError("Http response is {0} {1}".format(resp.status, resp.reason))

            data = resp.read()
            self.logger.debug("Response body is {0}".format(data))

            result = json.loads(data)
            self.logger.debug("Parsed result is {0}".format(result))
            return result
        finally:
            conn.close()
