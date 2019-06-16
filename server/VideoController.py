import logging
import subprocess
import time
import picamera

class VideoController:
    def __init__(self, config):
        self.logger = logging.getLogger("VideoController")
        self.ports = range(config['PortRange']['first'], config['PortRange']['last'])
        self.host = config['host']
        self.devices = config['Devices']
        self.width = config['width']
        self.height = config['height']
        self.bitrate = config['bitrate']
        self.fps = config['fps']
        self.captures = {}


    def start(self):
        self.logger.info("Starting")
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.stopAllCaptures()
        self.logger.info("Stopped")

    def startCapture(self, name, width, height, bitrate, fps, host):
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
        args = [width, height,
                bitrate, fps,
                host, port
                ]

        self.logger.info("Starting raspivid with args: {0}".format(args))

        raspivid = subprocess.Popen([
            'gst-launch', '-v',
            'fdsrc',
            '!', 'h264parse',
            '!', 'rtph264pay', 'config-interval=10', 'pt=96',
            '!', 'udpsink', 'host={0}'.format(host), 'port={0}'.format(port)
        ], stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        # initialize the camera
        self.camera = picamera.PiCamera(resolution=(width, height), framerate=fps)
        self.camera.hflip = True

        # start recording to gstreamer's stdin
        self.camera.start_recording(raspivid.stdin, format='h264', bitrate=bitrate)

        self.logger.info("raspivid started")
        self.captures[name] = (raspivid, device, width, height, bitrate, fps, host, port)
        self.logger.info("Capture started at {0}".format(name))
        return port

    def stopCapture(self, name):
        if name not in self.captures:
            return

        (raspivid, device, width, height, bitrate, fps, host, port) = self.captures.pop(name)

        self.logger.info("Stopping capture at {0}".format(name))
        self.camera.stop_recording()
        self.camera.close()
        raspivid.terminate()
        raspivid.stdin.close()
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
            (raspivid, device, width, height, bitrate, fps, host, port) = params
            result.append({'name': name, 'device': device, 'width': width, 'height': height,
                           'bitrate': bitrate, 'fps': fps, 'port': port, 'host': host})
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
            host = args.get('host')
            width = int(args.get('width'))
            height = int(args.get('height'))
            bitrate = int(args.get('bitrate'))
            fps = int(args.get('fps'))
            port = self.videoController.startCapture(name, width, height, bitrate, fps, host)
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
