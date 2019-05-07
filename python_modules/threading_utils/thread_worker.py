# -*- coding: utf-8 -*-

import threading
import traceback


class ThreadWorker:
    def __init__(self, name, logger, workerDone):
        self.name = name
        self.workerDone = workerDone
        self.logger = logger
        self.command = None
        self.thread = threading.Thread(target=self.threadProc, name=self.name)
        self.thread.daemon = True

        self.stopFlag = False
        self.waitLock = threading.Lock()
        self.handleLock = threading.Lock()

    def __str__(self):
        return self.name

    def start(self):
        self.logger.debug("{0}: Starting worker".format(self))
        self.stopFlag = False

        self.waitLock.acquire()
        self.thread.start()

        self.logger.debug("{0}: Worker started".format(self))

    def stop(self):
        self.logger.debug("{0}: Stopping worker".format(self))
        self.stopFlag = True
        self.waitLock.release()
        self.thread.join()
        self.logger.debug("{0}: Worker stopped".format(self))

    def do(self, command):
        self.logger.debug("{0}: Scheduling {1}".format(self, command))
        with self.handleLock:
            self.command = command
            self.waitLock.release()

    def threadProc(self):
        self.logger.debug("{0}: Thread proc started".format(self))
        while not self.stopFlag:
            self.logger.debug("{0}: Waiting for command".format(self))
            self.waitLock.acquire()
            command = self.command
            self.command = None

            if command is None:
                continue

            self.logger.debug("{0}: Got {1}".format(self, command))

            with self.handleLock:
                try:
                    self.logger.debug("{0}: Executing command {1}".format(self, command))
                    command.execute()
                    self.logger.debug("{0}: Executed {1}".format(self, command))
                except Exception as ex:
                    self.logger.warning("{0}: Exception caught: {1}\n{2}".format(ex, traceback.format_exc()))

            self.workerDone(self)
        self.logger.debug("{0}: Thread proc ended".format(self))