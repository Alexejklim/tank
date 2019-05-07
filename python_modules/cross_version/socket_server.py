from sys import version_info

if version_info[0] > 2:
    from socketserver import *
else:
    from SocketServer import *