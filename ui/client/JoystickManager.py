import threading
import time

import pygame

from Joystick import *
from python_modules.common_utils import MulticastDelegate


class JoystickManager:
    def __init__(self, updateInterval):
        self.logger = logging.getLogger("JoystickManager")
        pygame.joystick.init()

        self.interval = updateInterval
        self.started = False
        self.thread = None
        self.EvJoystickUpdate = MulticastDelegate()

    def createJoystick(self, id):
        return Joystick(self, id)

    @staticmethod
    def getAvailableJoystics():
        result = {}
        for n in range(pygame.joystick.get_count()):
            j = pygame.joystick.Joystick(n)
            result[n] = j.get_name()
        return result

    def start(self):
        if self.thread is not None:
            raise RuntimeError("Already started")

        self.logger.debug("Starting")
        self.thread = threading.Thread(target=self.threadProc)
        self.thread.daemon = True
        self.started = True
        self.thread.start()
        self.logger.debug("Started")

    def stop(self):
        if not self.started:
            return
        self.logger.debug("Stopping")
        self.started = False
        self.thread.join()
        self.thread = None
        self.logger.debug("Stopped")

    def threadProc(self):
        while self.started:
            try:
                for event in pygame.event.get():
                    pass

                self.EvJoystickUpdate()
                time.sleep(self.interval)
            except Exception, ex:
                self.logger.error("{0}: Exception caught: {1}\n{2}".format(self, ex, traceback.format_exc()))
