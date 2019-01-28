import json
import logging
import time
import traceback
import threading
import socket

class InfoController:
    def __init__(self, config):
        self.logger = logging.getLogger("InfoController")
        self.interval = config['interval']
        self.infos = {}
        self.started = False
        self.thread = None
        self.lock = None

        self.infoReceivers = {}

    def addAll(self, names, getFunction):
        for name in names:
            self.addInfo(name, getFunction)

    # getFunction should return (type, value)
    def addInfo(self, name, getFunction):
        if name in self.infos:
            raise RuntimeError("Info {0} already exists".format(name))

        self.infos[name] = getFunction

    def delInfo(self, name):
        if name not in self.infos:
            raise RuntimeError("Wrong info name: {0}".format(name))

        self.infos.pop(name)

    def start(self):
        if self.thread is not None:
            raise RuntimeError("Already started")

        self.logger.info("Starting")

        self.logger.info("Creating socket")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(1)

        self.lock = threading.Lock()
        self.logger.info("Starting thread")
        self.thread = threading.Thread(target=self.threadProc)
        self.thread.daemon = True
        self.started = True
        self.thread.start()
        self.logger.info("Started")

    def stop(self):
        if not self.started:
            return
        self.logger.info("Stopping")
        self.started = False
        self.thread.join()
        self.thread = None
        self.lock = None
        self.socket.close()
        self.socket = None
        self.clearInfoReceivers()
        self.logger.info("Stopped")

    def addInfoReceiver(self, addr):
        with self.lock:
            if addr in self.infoReceivers:
                RuntimeError("Already sending info to {0}".format(addr))
            self.infoReceivers[addr] = True

    def delInfoReceiver(self, addr):
        with self.lock:
            if addr in self.infoReceivers:
                self.infoReceivers.pop(addr)

    def clearInfoReceivers(self):
        with self.lock:
            for sender in self.infoReceivers.itervalues():
                sender.dispose()
            self.infoReceivers.clear()

    def clearInfos(self):
        self.logger.info("Clearing infos")
        self.infos.clear()

    def getInfos(self):
        infos = {}

        for name, fn in self.infos.iteritems():
            type, value = fn()
            infos[name] = {'type': type, 'value': value}

        return infos

    def getStatus(self):
        infos = self.getInfos()

        with self.lock:
            receivers = self.infoReceivers.keys()

        return {"infos": infos, "receivers": receivers}

    def threadProc(self):
        while self.started:
            try:
                infos = self.getInfos()

                jsonData = jsonData.dumps(infos)

                with self.lock:
                    receivers = self.infoReceivers.keys()

                for addr in receivers:
                    self.socket.sendto(jsonData, addr)

                time.sleep(self.interval)
            except Exception, ex:
                self.logger.error("{0}: Exception caught: {1}\n{2}".format(self, ex, traceback.format_exc()))


class InfoCommandHandler:
    def __init__(self, infoController):
        self.infoController = infoController

    def handleCommand(self, cmd, args):
        if cmd != 'info':
            raise NotImplementedError("Wrong command: {0}".format(cmd))

        action = args.get('act')

        if action == 'status':
            return {'infoStatus': self.infoController.getStatus()}

        elif action == 'start':
            self.infoController.start()
            return True
        elif action == 'stop':
            self.infoController.stop()
            return True

        else:
            raise NotImplementedError("Wrong action: {0}".format(action))
