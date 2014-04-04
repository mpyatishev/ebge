# -*- coding: utf-8 -*-

import curses
import random
import sys

from time import sleep

import components
import systems

from engine.engine import Engine
from engine.entity import EntityManager

class Image:
    def __init__(self, window):
        self.window = window

class SpaceShipImage(Image):
    def draw(self, position):
        try:
            y = int(position.y)
            x = int(position.x)
            self.window.addstr(y, x + 1, 'O')
            self.window.addstr(y + 1, x + 1, '|')
            self.window.addstr(y + 1, x + 2, '=')
            self.window.addstr(y + 1, x + 3, '^')
            self.window.addstr(y + 1, x + 4, '>')
            self.window.addstr(y + 2, x, '/')
            self.window.addstr(y + 2, x + 2, '\\')
        except Exception as e:
            self.window.addstr(str(e))
            self.window.addstr(str(position.y))
            self.window.addstr(str(position.x))
            self.window.refresh()
            self.window.getkey()


class RockImage(Image):
    def draw(self, position):
        try:
            self.window.addstr(int(position.y), int(position.x), '*')
        except Exception as e:
            print(e, int(position.y), int(position.x))

engine = Engine()

def main(window):
    window.clear()
    window.addstr('test string')
    maxyx = window.getmaxyx()

    em = EntityManager()

    engine.add_system(systems.MovementSystem(em), 1)
    engine.add_system(systems.RenderSystem(em, maxyx), 2)

    spaceship = em.create_entity(name='SpaceShip')
    em.add_component(components.Position(x=1, y=10), spaceship)
    em.add_component(components.Display(view=SpaceShipImage(window)), spaceship)

    for i in range(10):
        rock = em.create_entity(name='Rock')
        em.add_component(components.Position(x=random.uniform(0, maxyx[1]),
                                             y=random.uniform(0, maxyx[0])),
                         rock)
        em.add_component(components.Display(view=RockImage(window)), rock)

    time = 0
    while time < 50:
        window.clear()
        engine.update(time)
        time += 1
        sleep(0.1)
        window.refresh()

    window.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
