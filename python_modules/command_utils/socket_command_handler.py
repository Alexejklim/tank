# -*- coding: utf-8 -*-

import logging
from .command_handler import CommandHandler
from ..server_utils import CreateTcpRequestHandlerRedirectorClass
from ..server_utils import CreateUdpRequestHandlerRedirectorClass

MAX_REQUEST_LEN = 65536


class SocketCommandHandler(CommandHandler):
    def __init__(self, commandHandlerDelegate=None):

        CommandHandler.__init__(self, commandHandlerDelegate)
        self.logger = logging.getLogger("SocketCommandHandler")

    def answer(self, requestHandler, result):
        response = self.prepareResponse(result)
        requestHandler.wfile.write(response)

    def handleRequest(self, requestHandler):
        requestString = requestHandler.rfile.readline(MAX_REQUEST_LEN + 1)
        if len(requestString) > MAX_REQUEST_LEN:
            self.answer(requestHandler, {'status': 'ERROR', 'error': 'Request too long'})
            return

        if not requestString:
            return

        requestString = requestString.rstrip('\r\n')

        (cmd, args) = self.parseRequestString(requestString)

        args['_remoteAddr'] = requestHandler.client_address

        result = self.callHandler(cmd, args)

        noAnswer = result.pop('_noAnswer', False)

        if not noAnswer:
            self.answer(requestHandler, result)


class TCPCommandHandler(SocketCommandHandler):
    def __init__(self, commandHandlerDelegate = None):
        SocketCommandHandler.__init__(self, commandHandlerDelegate)
        self.logger = logging.getLogger("TCPCommandHandler")
        self.protocol = 'tcp'

    def getRequestHandlerClass(self):
        return CreateTcpRequestHandlerRedirectorClass(self.handleRequest)


class UDPCommandHandler(SocketCommandHandler):
    def __init__(self, commandHandlerDelegate = None):
        SocketCommandHandler.__init__(self, commandHandlerDelegate)
        self.logger = logging.getLogger("UDPCommandHandler")
        self.protocol = 'udp'

    def getRequestHandlerClass(self):
        return CreateUdpRequestHandlerRedirectorClass(self.handleRequest)
