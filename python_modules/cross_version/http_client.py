from sys import version_info

if version_info[0] > 2:
    from http.client import *
else:
    from httplib import *