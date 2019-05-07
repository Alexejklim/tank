# -*- coding: utf-8 -*-
from ..cross_version.socket_server import TCPServer
from ..cross_version.socket_server import UDPServer
from ..cross_version.http_server import HTTPServer

from .mixins import DispatchedServerMixIn, BackgroundServerMixIn


__all__ = ['DispatchedTCPServer',
           'DispatchedUDPServer',
           'DispatchedHTTPServer',
           'DispatchedBackgroundTCPServer',
           'DispatchedBackgroundUDPServer',
           'DispatchedBackgroundHTTPServer']


class DispatchedTCPServer(DispatchedServerMixIn, TCPServer):
    def __init__(self, server_address, RequestHandlerClass, dispatcher, bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.dispatcher = dispatcher


class DispatchedUDPServer(DispatchedServerMixIn, UDPServer):
    def __init__(self, server_address, RequestHandlerClass, dispatcher, bind_and_activate=True):
        UDPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.dispatcher = dispatcher


class DispatchedHTTPServer(DispatchedTCPServer, HTTPServer):
    pass


class DispatchedBackgroundTCPServer(DispatchedServerMixIn, BackgroundServerMixIn, TCPServer):
    def __init__(self, server_address, RequestHandlerClass, dispatcher):
        TCPServer.__init__(self, server_address, RequestHandlerClass, False)
        self.dispatcher = dispatcher


class DispatchedBackgroundUDPServer(DispatchedServerMixIn, BackgroundServerMixIn, UDPServer):
    def __init__(self, server_address, RequestHandlerClass, dispatcher):
        UDPServer.__init__(self, server_address, RequestHandlerClass, False)
        self.dispatcher = dispatcher


class DispatchedBackgroundHTTPServer(DispatchedBackgroundTCPServer, HTTPServer):
    pass