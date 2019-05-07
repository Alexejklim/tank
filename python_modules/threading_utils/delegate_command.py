# -*- coding: utf-8 -*-


class DelegateCommand:
    def __init__(self, method, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.method = method

    def execute(self):
        self.method(*self.args, **self.kwargs)

    def __str__(self):
        return "{0} {1} {2}".format(self.method, self.args, self.kwargs)