# -*- coding: utf-8 -*-

import curses
import random
# import sys

from time import sleep

import components
import systems

from engine.engine import Engine
from engine.entity import EntityManager


class Image:
    def __init__(self, window):
        self.window = window


class SpaceShipImage(Image):
    def __init__(self, window):
        super().__init__(window)

        self.frame_time = 0.09
        self.frame_count = 3
        self.frames = [()] * self.frame_count

        self.frames[0] = (
            (0, 1, 'O'),
            (1, 1, '|'),
            (1, 2, '='),
            (1, 3, '^'),
            (1, 4, '>'),
            (2, 0, ' '),
            (2, 1, '||'),
            (2, 2, ' '),
            # (2, 0, '/'),
            # (2, 2, '\\'),
        )
        self.frames[1] = (
            (0, 1, 'O'),
            (1, 1, '|'),
            (1, 2, '='),
            (1, 3, '^'),
            (1, 4, '>'),
            (2, 1, '|'),
            (2, 2, '\\'),
        )
        self.frames[2] = (
            (0, 1, 'O'),
            (1, 1, '|'),
            (1, 2, '='),
            (1, 3, '^'),
            (1, 4, '>'),
            (2, 0, '/'),
            (2, 1, '|'),
            (2, 2, ' '),
        )

    def draw(self, position, time):
        try:
            y = int(position.y)
            x = int(position.x)

            for sprite in self.frames:
                for el in sprite:
                    self.window.addstr(y + el[0], x + el[1], el[2])
                self.window.addstr(y + 3, x, 'y = %s, x = %s' % (y, x))
                self.window.refresh()
                sleep(abs(self.frame_time / self.frame_count))
            for el in self.frames[0]:
                self.window.addstr(y + el[0], x + el[1], el[2])

        except Exception as e:
            self.window.addstr(str(e))
            self.window.addstr(str(position.y))
            self.window.addstr(str(position.x))
            self.window.refresh()
            # self.window.getkey()


class RockImage(Image):
    def draw(self, position, time):
        try:
            self.window.addstr(int(position.y), int(position.x), '*')
            self.window.refresh()
        except Exception as e:
            print(e, int(position.y), int(position.x))

engine = Engine()


def main(window):
    window.clear()
    window.addstr('test string')
    maxyx = window.getmaxyx()
    window.nodelay(True)

    em = EntityManager()

    engine.add_system(systems.InputSystem(em), 0)
    engine.add_system(systems.MovementSystem(em), 1)
    engine.add_system(systems.RenderSystem(em, maxyx), 2)

    spaceship = em.create_entity(name='SpaceShip')
    em.add_component(components.Input(window=window), spaceship)
    em.add_component(components.Position(x=1, y=10), spaceship)
    em.add_component(components.Velocity(), spaceship)
    em.add_component(components.Display(view=SpaceShipImage(window)), spaceship)

    for i in range(5):
        rock = em.create_entity(name='Rock')
        em.add_component(components.Position(x=random.uniform(0, maxyx[1]),
                                             y=random.uniform(0, maxyx[0])),
                         rock)
        em.add_component(components.Display(view=RockImage(window)), rock)

    time = 0
    while True:
        window.clear()
        engine.update(time)
        time += 1

    # window.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
