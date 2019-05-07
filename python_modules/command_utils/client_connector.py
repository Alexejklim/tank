# -*- coding: utf-8 -*-

import logging


class ClientConnector:
    def __init__(self):
        self.logger = logging.getLogger("ClientConnector")

    def __del__(self):
        self.dispose()

    def request(self, request, params):
        self.logger.debug("Making request string for request {0}".format(request))
        requestString = "/{0}?".format(request)

        for (key, value) in params.iteritems():
            # TODO: add something like UriEscape()
            requestString += "{0}={1}&".format(key, value)

        self.logger.debug("Executing request {0}".format(requestString))
        result = self._doRequest(requestString)

        self.logger.debug("Result is {0}".format(result))
        return result

    def _doRequest(self, requestString):
        pass

    def requestAndCheck(self, request, params):
        result = self.request(request, params)

        if result is None:
            raise RuntimeError("Result is None")

        if result['status'] != 'OK':
            raise RuntimeError("Response status is {0}".format(result['status']))

        return result

    def dispose(self):
        pass
