# -*- coding: utf-8 -*-

import curses

from engine.component import Component


class Position(Component):
    def __init__(self, x=0.0, y=0.0, rotation=0):
        self.x = x
        self.y = y
        self.rotation = rotation


class Velocity(Component):
    def __init__(self, x=0.0, y=0.0, ang=0.0):
        self.velocity_x = x
        self.velocity_y = y
        self.angular_velocity = ang


class Display(Component):
    def __init__(self, x=0.0, y=0.0, view=None):
        self.x = x
        self.y = y
        self.view = view


class Input(Component):
    KEY_UP = curses.KEY_UP
    KEY_DOWN = curses.KEY_DOWN
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT

    def __init__(self, window=None):
        self.window = window

    def get_key(self):
        return self.window.get_wch()
