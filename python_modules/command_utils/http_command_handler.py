# -*- coding: utf-8 -*-
import copy
import logging

from ..server_utils import CreateHttpRequestHandlerRedirectorClass
from .command_handler import CommandHandler
import six

class HTTPCommandHandler(CommandHandler):
    def __init__(self, commandHandlerDelegate=None):
        CommandHandler.__init__(self, commandHandlerDelegate)
        self.logger = logging.getLogger("HTTPCommandHandler")
        self.protocol = 'http'

    def getRequestHandlerClass(self):
        requestHandlerClass = CreateHttpRequestHandlerRedirectorClass(self.handleRequest)
        requestHandlerClass.protocol_version = "HTTP/1.1"
        return requestHandlerClass

    def handleRequest(self, requestHandler):
        requestString = requestHandler.path
        self.logger.debug("Request received: {0}".format(requestString))

        (cmd, args) = self.parseRequestString(requestString)

        args['_httpMethod'] = requestHandler.command
        args['_remoteAddr'] = requestHandler.client_address
        args['_httpHeaders'] = copy.copy(requestHandler.headers)

        if requestHandler.command == 'GET':
            args['_httpBody'] = requestHandler.rfile.read(int(requestHandler.headers.get('Content-Length')))

        result = self.callHandler(cmd, args)

        httpCode = None
        if result['status'] == 'OK':
            httpCode = 200
        elif result['status'] == 'NOTFOUND':
            httpCode = 404
        elif result['status'] == 'ERROR':
            httpCode = 500

        httpCode = result.pop('_httpCode', httpCode)
        contentType = result.pop('_httpContentType', 'text/json')
        headers = result.pop('_httpHeaders', {})

        response = self.prepareResponse(result)

        requestHandler.send_response(httpCode)
        requestHandler.send_header('Content-Type', contentType)
        requestHandler.send_header('Connection', 'keep-alive')
        requestHandler.send_header('Content-Length', len(response))

        for (key, value) in six.iteritems(headers):
            requestHandler.send_header(key, value)

        requestHandler.end_headers()
        requestHandler.wfile.write(six.b(response))