# -*- coding: utf-8 -*-


class MulticastDelegate:
    def __init__(self):
        self.delegates = []

    def add(self, delegate):
        self.delegates.append(delegate)

    def sub(self, delegate):
        self.delegates.remove(delegate)

    def __iadd__(self, delegate):
        self.add(delegate)
        return self

    def __isub__(self, delegate):
        self.sub(delegate)
        return self

    def __call__(self, *args, **kwargs):
        for d in self.delegates:
            d(*args, **kwargs)
