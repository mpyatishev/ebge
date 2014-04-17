# -*- coding: utf-8 -*-


from engine.system import System


class MovementSystem(System):
    def update(self, time):
        em = self.entity_manager
        for entity in em.get_entities_by_component_class('Position'):
            position = em.get_component('Position', entity)
            velocity = em.get_component('Velocity', entity)

            if velocity:
                position.x += velocity.velocity_x
                position.y += velocity.velocity_y

                velocity.velocity_x = 0
                velocity.velocity_y = 0

            render = em.get_component('Display', entity)
            if render:
                render.x = position.x
                render.y = position.y


class RenderSystem(System):
    def __init__(self, entity_manager=None, maxyx=(0, 0)):
        super().__init__(entity_manager=entity_manager)
        self.maxyx = maxyx

    def update(self, time):
        em = self.entity_manager
        for entity in em.get_entities_by_component_class('Display'):
            render = em.get_component('Display', entity)
            position = em.get_component('Position', entity)

            if render.y >= self.maxyx[0]:
                render.y = 0
                position.y = 0
            if render.y < 0:
                render.y = 0
                position.y = 0
            if render.x >= self.maxyx[1]:
                render.x = 0
                position.x = 0
            if render.x < 0:
                render.x = 0
                position.x = 0

            render.view.draw(render, time)


import curses


class InputSystem(System):
    def update(self, time):
        em = self.entity_manager

        for entity in em.get_entities_by_component_class('Input'):
            input = em.get_component('Input', entity)
            velocity = em.get_component('Velocity', entity)

            if not velocity:
                continue

            try:
                key = input.window.get_wch()
            except:
                return

            if key == curses.KEY_UP:
                velocity.velocity_y = -1
            if key == curses.KEY_DOWN:
                velocity.velocity_y = 1
            elif key == curses.KEY_RIGHT:
                velocity.velocity_x = 1
            elif key == curses.KEY_LEFT:
                velocity.velocity_x = -1
