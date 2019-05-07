# -*- coding: utf-8 -*-
import subprocess
import threading

import logging
import traceback

import time


class ProcessDataPipe(object):
    def __init__(self, args, outStream, errStream=None, shell=False):
        self.logger = logging.getLogger("ProcessDataPipe[{0}]".format(self.__hash__()))
        self.args = args
        self.shell = shell
        self.outStream = outStream
        self.errStream = errStream

        self.stopThread = None
        self.thread = threading.Thread(target=self.threadProc, name="ProcessDataPipe")
        self.thread.daemon = True

        self.process = None

    def start(self):
        self.logger.info("Starting")
        self.process = subprocess.Popen(self.args, shell=self.shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE if self.errStream else None)
        self.stopThread = False
        self.thread.start()
        self.logger.info("Started")

    def getInputStream(self):
        return self.process.stdin

    def stop(self):
        self.logger.info("Stopping")
        self.process.stdin.close()
        self.process.wait()
        self.stopThread = True
        self.thread.join()
        self.logger.info("Stopped")

    def threadProc(self):
        while not self.stopThread:
            try:
                idle = True

                buf = self.process.stdout.read(8192)
                if buf:
                    idle = False
                self.outStream.write(buf)

                if self.errStream:
                    buf = self.process.stderr.read(8192)
                    if buf:
                        idle = False
                    self.errStream.write(buf)

                if idle:
                    time.sleep(0.01)

            except Exception as ex:
                self.logger.warning("Exception caught in thread proc: {1}\n{2}".format(ex, traceback.format_exc()))
