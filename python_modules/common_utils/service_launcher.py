# -*- coding: utf-8 -*-

import signal
import time
import traceback

from ..common_utils.util_launcher import UtilLauncher


class DummyService:
    def __init__(self, config):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class ServiceRunnable:
    def __init__(self, config, serviceLauncher):
        self.config = config
        self.logger = serviceLauncher.logger
        self.serverLauncher = serviceLauncher

        self.needStop = False

        def onInt(*a):
            self.needStop = True

        signal.signal(signal.SIGINT, onInt)
        signal.signal(signal.SIGTERM, onInt)

    def stop(self):
        self.logger.info("Manual stop requested")
        self.needStop = True

    def run(self):
        self.logger.info("Creating service")

        service = self.serverLauncher.createService(self.config)

        self.needStop = False
        try:
            self.logger.info("Starting service")
            service.start()
            self.logger.info("Service started")

            while not self.needStop:
                self.serverLauncher.idle()

        except Exception as ex:
            self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))

            self.logger.info("Stopping service")

        service.stop()
        self.logger.info("Service stopped")


class ServiceLauncher(UtilLauncher):
    def __init__(self):
        UtilLauncher.__init__(self)
        self.runnable = None

    def createService(self, config):
        return DummyService(config)

    def createUtil(self, config):
        self.runnable = ServiceRunnable(config, self)
        return self.runnable

    def idle(self):
        time.sleep(0.1)

    def stop(self):
        if self.runnable:
            self.runnable.stop()

    def Run(self, changeDir = True):
        UtilLauncher.Run(self, changeDir)