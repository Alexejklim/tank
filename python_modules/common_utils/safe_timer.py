# -*- coding: utf-8 -*-
import threading
import logging
import traceback


class SafeTimer:
    def __init__(self, handler, interval, name = "noname"):
        self.logger = logging.getLogger("SafeTimer[{0}]".format(name))
        self.handler = handler
        self.interval = interval
        self.name = name

        self.processing = False
        self.timer = None
        self.lock = threading.Lock()

    def __del__(self):
        self.stop()

    def start(self, now = False):
        if self.timer is not None:
            raise Exception("Timer {0} already started".format(self.name))

        self.logger.debug("Starting timer {0}".format(self.name))

        if now:
            self.timerProc()
        else:
            self.timer = threading.Timer(self.interval, self.timerProc)
            self.timer.start()

    def stop(self):
        self.logger.debug("Stopping timer {0}".format(self.name))
        with self.lock:
            if self.timer is not None:
                self.timer.cancel()
                self.timer = None

    def timerProc(self):
        with self.lock:
            if self.timer is not None:
                self.timer = threading.Timer(self.interval, self.timerProc)
                self.timer.start()

            if self.processing:
                self.logger.debug("Already processing handler")
                return
            self.processing = True

        try:
            self.logger.debug("Executing timer handler {0}".format(self.handler))
            self.handler()
            self.logger.debug("Timer handler done")
        except Exception as ex:
            self.logger.warning("Exception caught while executing timer handler {0}: {1}\n{2}"
                                .format(self.handler, ex, traceback.format_exc()))
        finally:
            with self.lock:
                self.processing = False