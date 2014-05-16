# -*- coding: utf-8 -*-


class IDisplayProvider:
    def get_maxx(self):
        pass

    def get_maxy(self):
        pass

    def get_maxxy(self):
        pass

    def get_up_direction(self):
        pass

    def get_down_direction(self):
        pass

    def get_right_direction(self):
        pass

    def get_left_direction(self):
        pass


class CursesDisplayProvider(IDisplayProvider):
    UP = -1
    DOWN = 1
    RIGHT = 1
    LEFT = -1

    def __init__(self, window):
        self.window = window
        self.maxyx = self.window.getmaxyx()

    def get_up_direction(self):
        return self.UP

    def get_down_direction(self):
        return self.DOWN

    def get_right_direction(self):
        return self.RIGHT

    def get_left_direction(self):
        return self.LEFT

    def get_maxxy(self):
        return (self.maxyx[1], self.maxyx[0])

    def get_maxx(self):
        return self.maxyx[1]

    def get_maxy(self):
        return self.maxyx[0]
