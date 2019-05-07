# -*- coding: utf-8 -*-

import threading
from ..threading_utils import DelegateCommand


class BackgroundServerMixIn:
    def startServer(self):
        self.server_bind()
        self.server_activate()

        self.serverThread = threading.Thread(target = self.serve_forever, name ="BackgroundServer")
        self.serverThread.daemon = True
        self.serverThread.start()
        
    def stopServer(self):
        if getattr(self, 'serverThread', None):
            self.shutdown()
            self.serverThread.join()
            self.serverThread = None
            self.server_close()


class DispatchedServerMixIn:
    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        cmd = DelegateCommand(self.process_request_thread, request, client_address)
        self.dispatcher.dispatch(cmd)