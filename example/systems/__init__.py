# -*- coding: utf-8 -*-


from engine.system import System


class MovementSystem(System):
    def update(self, time):
        component_class = 'Position'
        em = self.entity_manager
        for entity in em.get_entities_by_component_class(component_class):
            component = em.get_component(component_class, entity)

            component.x += component.velocity_x
            component.y += component.velocity_y

            component.velocity_x = 0
            component.velocity_y = 0

            render = em.get_component('Display', entity)
            if render:
                render.x = component.x
                render.y = component.y


class RenderSystem(System):
    def __init__(self, entity_manager=None, maxyx=(0, 0)):
        super().__init__(entity_manager=entity_manager)
        self.maxyx = maxyx

    def update(self, time):
        component_class = 'Display'
        em = self.entity_manager
        for entity in em.get_entities_by_component_class(component_class):
            component = em.get_component(component_class, entity)
            position = em.get_component('Position', entity)

            if component.y >= self.maxyx[0]:
                component.y = 0
                position.y = 0
            if component.y < 0:
                component.y = 0
                position.y = 0
            if component.x >= self.maxyx[1]:
                component.x = 0
                position.x = 0
            if component.x < 0:
                component.x = 0
                position.x = 0

            component.view.draw(component, time)


import curses


class InputSystem(System):
    component_class = 'Input'

    def update(self, time):
        em = self.entity_manager

        for entity in em.get_entities_by_component_class(self.component_class):
            component = em.get_component(self.component_class, entity)
            position = em.get_component('Position', entity)

            if not position:
                continue

            try:
                key = component.window.get_wch()
            except:
                return

            if key == curses.KEY_UP:
                position.velocity_y = -1
            if key == curses.KEY_DOWN:
                position.velocity_y = 1
            elif key == curses.KEY_RIGHT:
                position.velocity_x = 1
            elif key == curses.KEY_LEFT:
                position.velocity_x = -1
