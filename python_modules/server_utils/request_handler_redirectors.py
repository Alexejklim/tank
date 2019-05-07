# -*- coding: utf-8 -*-

from ..cross_version.http_server import *
from ..cross_version.socket_server import *

__all__ = ['CreateHttpRequestHandlerRedirectorClass',
           'CreateTcpRequestHandlerRedirectorClass',
           'CreateUdpRequestHandlerRedirectorClass']

defaultHttpMethods = ['GET', 'POST']


def CreateHttpRequestHandlerRedirectorClass(handlerDelegate, methods = defaultHttpMethods):
    class HttpRedirector(BaseHTTPRequestHandler):
        def __getattr__(self, item):
            if item in HttpRedirector.supportedMethods:
                return self.doMethod
            else:
                raise AttributeError()

        def doMethod(self):
            HttpRedirector.handlerDelegate(self)

    HttpRedirector.supportedMethods = []
    for method in methods:
        HttpRedirector.supportedMethods.append('do_' + method)

    HttpRedirector.handlerDelegate = handlerDelegate
    HttpRedirector.protocol_version = "HTTP/1.1"

    return HttpRedirector


def CreateTcpRequestHandlerRedirectorClass(handlerDelegate):
    class Redirector(StreamRequestHandler):
        def handle(self):
            Redirector.handleRequest(self)

    Redirector.handleRequest = handlerDelegate
    return Redirector


def CreateUdpRequestHandlerRedirectorClass(handlerDelegate):
    class Redirector(DatagramRequestHandler):
        def handle(self):
            Redirector.handleRequest(self)

    Redirector.handleRequest = handlerDelegate
    return Redirector
