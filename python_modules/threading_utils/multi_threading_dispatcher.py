# -*- coding: utf-8 -*-

import logging

from six.moves import queue as Queue

from .thread_worker import ThreadWorker


class MultiThreadingDispatcher:
    def __init__(self, name, threadsNumber, maxQueueSize = 0):
        self.name = name
        self.threadsNumber = threadsNumber
        self.maxQueueSize = maxQueueSize
        self.commandsQueue = Queue.Queue(self.maxQueueSize)

        self.workersQueue = Queue.Queue()
        self.freeWorkersQueue = Queue.Queue()
        self.logger = logging.getLogger("MultiThreadingDispatcher")

    def __str__(self):
        return self.name

    def start(self):
        self.logger.debug("{0}: Starting dispatcher".format(self))
        for n in range(self.threadsNumber):
            worker = ThreadWorker("{0} Worker #{1}".format(self, n), self.logger, self.__workerDone)
            worker.start()
            self.workersQueue.put(worker)
            self.__workerDone(worker)
        self.logger.debug("{0}: Dispatcher started".format(self))

    def stop(self):
        self.logger.debug("{0}: Stopping dispatcher".format(self))
        while True:
            try:
                worker = self.workersQueue.get_nowait()
                worker.stop()
            except Queue.Empty:
                break
        self.logger.debug("{0}: Dispatcher stopped".format(self))

    def dispatch(self, command):
        self.logger.debug("{0}: Dispatching command {1}".format(self, command))
        try:
            worker = self.freeWorkersQueue.get_nowait()
            worker.do(command)
        except Queue.Empty:
            try:
                self.logger.debug("{0}: All workers are busy, enqueueing {1}".format(self, command))
                self.commandsQueue.put_nowait(command)
            except Queue.Full:
                self.logger.warning("{0}: Command queue is full, dropping {1}".format(self, command))
            self.logger.debug("{0}: Command queue size: {1}, Free workers: {2}".format(self, self.commandsQueue.qsize(),
                                                                                       self.freeWorkersQueue.qsize()))

    def __workerDone(self, worker):
        self.logger.debug("{0}: Worker {1} is done".format(self, worker))
        try:
            command = self.commandsQueue.get_nowait()
            worker.do(command)
        except Queue.Empty:
            self.logger.debug("{0}: Worker {1} is free now".format(self, worker))
            self.freeWorkersQueue.put(worker)
        self.logger.debug("{0}: Command queue size: {1}, Free workers: {2}".format(self, self.commandsQueue.qsize(),
self.freeWorkersQueue.qsize()))