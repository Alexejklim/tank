import logging
import subprocess
import time


class VideoController:
    def __init__(self, config):
        self.logger = logging.getLogger("VideoController")

        self.ports = range(config['PortRange']['first'], config['PortRange']['last'])
        self.listenHost = config['listenHost']
        self.devices = config['Devices']
        self.wight = config['wight']
        self.height = config['height']
        self.bitrate = config['bitrate']
        self.fps = config['fps']
        self.captures = {}


    def start(self):
        self.logger.info("Starting")

        port = self.ports.pop(0)
        args = [self.wight, self.height
               ,self.bitrate, self.fps,
                self.listenHost, port]

        self.logger.info("Starting raspivid with args: {0}".format(args))

        gstreamer = ('raspivid -n -w {0} -h {1} -b {2} -fps {3} -vf -hf -t 0 -o  - | gst-launch -v fdsrc ! h264parse !'+
                     'rtph264pay config-interval=10 pt=96 ! udpsink host={4} port={5}').format(self.wight, self.height
               ,self.bitrate, self.fps,
                self.listenHost, port)
        raspivid = subprocess.Popen(gstreamer, shell = True)

        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.stopAllCaptures()
        self.logger.info("Stopped")

    def startCapture(self, name, width, height, fps):
        if name not in self.devices:
            raise RuntimeError("Invalid name: {0}".format(name))

        if name in self.captures:
            raise RuntimeError("Capture already started at {0}".format(name))

        if len(self.ports) == 0:
            raise RuntimeError("No more ports available")

        self.logger.info("Starting capture at {0}".format(name))

        device = self.devices[name]

        port = self.ports.pop(0)



        self.logger.info("Waiting for raspivid to open port")
        time.sleep(1)
        self.logger.info("raspivid started")

        # self.captures[name] = (raspivid, device, width, height, fps, port)

        self.logger.info("Capture started at {0}".format(name))
        return port

    def stopCapture(self, name):
        if name not in self.captures:
            return

        (raspivid, device, width, height, fps, port) = self.captures.pop(name)

        self.logger.info("Stopping capture at {0}".format(name))

        raspivid.terminate()
        raspivid.wait()

        self.logger.info("Capture stopped at {0}".format(name))
        self.ports.append(port)

    def stopAllCaptures(self):
        self.logger.info("Stopping all captures")
        for name in self.captures.keys():
            self.stopCapture(name)

    def getStatus(self):
        result = []

        for (name, params) in self.captures.iteritems():
            (raspivid, device, width, height, fps, port) = params
            result.append({'name': name, 'device': device, 'width': width, 'height': height, 'fps': fps, 'port': port})

        return {'devices': self.devices, 'captures': result}


class VideoCommandHandler:
    def __init__(self, videoController):
        self.videoController = videoController

    def handleCommand(self, cmd, args):
        if cmd != 'video':
            raise NotImplementedError("Wrong command: {0}".format(cmd))

        action = args.get('act')

        if action == 'startCapture':
            name = args.get('name')
            width = int(args.get('width'))
            height = int(args.get('height'))
            fps = int(args.get('fps'))
            port = self.videoController.startCapture(name, width, height, fps)

            return {'port': port}

        elif action == 'stopCapture':
            name = args.get('name')
            self.videoController.stopCapture(name)
            return True

        elif action == 'status':
            return {'videoStatus': self.videoController.getStatus()}

        elif action == 'start':
            self.videoController.start()
            return True
        elif action == 'stop':
            self.videoController.stop()
            return True

        else:
            raise NotImplementedError("Wrong action: {0}".format(action))
