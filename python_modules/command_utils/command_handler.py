# -*- coding: utf-8 -*-

import logging
import json
import traceback

import six
from six.moves import urllib_parse as urlparse


class CommandHandler:
    def __init__(self, commandHandlerDelegate=None):
        self.logger = logging.getLogger("BaseCommandHandler")
        self.commandHandlerDelegate = commandHandlerDelegate

        self.commandRouteTable = {}

    def setHandler(self, cmd, commandHandlerDelegate):
        self.commandRouteTable[cmd] = commandHandlerDelegate

    def parseRequestString(self, requestString):
        self.logger.debug("Parsing request string {0}".format(requestString))

        split = urlparse.urlsplit(requestString)
        args = urlparse.parse_qs(split.query, True)

        for key in six.iterkeys(args):
            args[key] = args[key][0]

        path = split.path.split("/")
        cmd = path[len(path) - 1]

        return cmd, args

    @staticmethod
    def prepareResponse(result):
        return json.dumps(result)

    def getHandler(self, cmd):
        return self.commandRouteTable.get(cmd, self.commandHandlerDelegate)

    def callHandler(self, cmd, args):
        self.logger.debug("Calling handler for command {0} with args {1}".format(cmd, args))
        try:
            handler = self.getHandler(cmd)
            if handler is None:
                self.logger.debug("Handler not found")
                return {'status': 'NOTFOUND', 'error': 'Command handler not found'}

            if hasattr(self, 'protocol'):
                args['_protocol'] = self.protocol

            result = handler(cmd, args)

            if isinstance(result, bool):
                if result:
                    return {'status': 'OK'}

                if not result:
                    return {'status': 'ERROR'}

            if 'status' not in result:
                result['status'] = 'OK'

            return result

        except Exception as ex:
            self.logger.error("{0}: Exception caught: {1}\n{2}".format(self, ex, traceback.format_exc()))
            return {'status': 'ERROR', 'error': str(ex)}