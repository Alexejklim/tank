from sys import version_info

if version_info[0] > 2:
    from http.server import *
else:
    from BaseHTTPServer import *