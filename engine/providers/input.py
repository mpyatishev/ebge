# -*- coding: utf-8 -*-


class IInputProvider:
    def get_key(self):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_right(self):
        pass

    def key_left(self):
        pass


import curses


class CursesInputProvider(IInputProvider):
    def __init__(self, window):
        self.window = window

    def get_key(self):
        return self.window.get_wch()

    def key_up(self):
        return curses.KEY_UP

    def key_down(self):
        return curses.KEY_DOWN

    def key_right(self):
        return curses.KEY_RIGHT

    def key_left(self):
        return curses.KEY_LEFT
