# -*- coding: utf-8 -*-

import logging
import threading
import traceback

import tornado.web
import tornado.httpserver
import tornado.ioloop


class TornadoSimpleWrapper:
    def __init__(self, handlers, config):
        self.logger = logging.getLogger("TornadoSimpleWrapper")
        self.config = config

        self.stopThread = None
        self.tornadoThread = threading.Thread(target=self.tornadoThreadProc, name="TornadoThread")
        self.tornadoApp = tornado.web.Application(handlers)

        if 'ssl_options' in self.config:
            self.tornadoHttpServer = tornado.httpserver.HTTPServer(self.tornadoApp, ssl_options=self.config['ssl_options'])

    def start(self):
        self.logger.info("Starting")
        self.tornadoApp.listen(self.config['port'], self.config['host'])
        self.stopThread = False
        self.tornadoThread.start()
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.stopThread = True
        tornado.ioloop.IOLoop.current().stop()
        self.tornadoThread.join()
        self.logger.info("Stopped")

    def tornadoThreadProc(self):
        self.logger.debug("Tornado thread proc started")

        while not self.stopThread:
            try:
                tornado.ioloop.IOLoop.current().start()
            except Exception as ex:
                self.logger.error(u"Exception caught in tornado thread: {0}\n{1}".format(ex, traceback.format_exc()))

        self.logger.debug("Tornado thread proc finished")