# -*- coding: utf-8 -*-

import curses
import random
# import sys
import logging

from time import sleep

import components
import systems

from engine.engine import Engine
from engine.entity import EntityManager
from engine.fsm import StateMachine
from engine.providers.input import CursesInputProvider
from engine.providers.display import CursesDisplayProvider


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('the_one.log', mode='w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


class Image(CursesDisplayProvider):
    pass


class ManStandImage(Image):
    def __init__(self, window):
        super().__init__(window)

        self.frame_time = 0.09
        self.frame_count = 1
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

    def draw(self, position, time):
        try:
            y = int(position.y)
            x = int(position.x)

            for el in self.frames[0]:
                self.window.addstr(y + el[0], x + el[1], el[2])

        except Exception as e:
            self.window.addstr(str(e))
            self.window.addstr(str(position.y))
            self.window.addstr(str(position.x))
            self.window.refresh()
            # self.window.getkey()


class ManWalkImage(Image):
    def __init__(self, window):
        super().__init__(window)

        self.frame_time = 0.09
        self.frame_count = 2
        self.frames = [()] * self.frame_count

        self.frames[0] = (
            (0, 1, 'O'),
            (1, 1, '|'),
            (1, 2, '='),
            (1, 3, '^'),
            (1, 4, '>'),
            (2, 1, '|'),
            (2, 2, '\\'),
        )
        self.frames[1] = (
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

            for frame in self.frames[time % self.frame_count]:
                self.window.addstr(y + frame[0], x + frame[1], frame[2])

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
        except Exception as e:
            print(e, int(position.y), int(position.x))


engine = Engine()


def create_the_one(em, window):
    logger.debug('creating the One')

    man = em.create_entity(name='Man')
    man_stand_view = ManStandImage(window)
    man_walk_view = ManWalkImage(window)
    # em.add_component(components.Input(window=window), man)
    # em.add_component(components.Position(x=1, y=10), man)
    # em.add_component(components.Velocity(), man)
    # em.add_component(components.Display(view=man_stand_view), man)

    input_provider = CursesInputProvider(window)

    fsm_man = StateMachine(em, man)
    fsm_man.create_state('stand')\
        .add(components.Input(input_provider))\
        .add(components.Position(x=1, y=10))\
        .add(components.Velocity())\
        .add(components.Display(view=man_stand_view))
    fsm_man.copy_state('stand', 'walk')\
        .remove(components.Display)\
        .add(components.Display(view=man_walk_view))
    fsm_man.change_state('stand')


def create_rocks(em, window, maxyx):
    logger.debug('creating the Rocks')
    for i in range(5):
        rock = em.create_entity(name='Rock%s' % i)
        em.add_component(components.Position(x=random.uniform(0, maxyx[1]),
                                             y=random.uniform(0, maxyx[0])),
                         rock)
        em.add_component(components.Display(view=RockImage(window)), rock)


def main(window):
    window.clear()
    window.addstr('test string')
    maxyx = window.getmaxyx()
    window.nodelay(True)

    em = EntityManager()

    engine.add_system(systems.InputSystem(em), 0)
    engine.add_system(systems.MovementSystem(em), 1)
    engine.add_system(systems.RenderSystem(em), 2)

    create_the_one(em, window)
    create_rocks(em, window, maxyx)

    time = 0
    while True:
        window.erase()

        engine.update(time)
        window.refresh()
        sleep(0.03)
        time += 1

    # window.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
