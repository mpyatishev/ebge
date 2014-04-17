# -*- coding: utf-8 -*-

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
    def __init__(self, window=None):
        self.window = window
