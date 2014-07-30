# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger()


class System:
    def __init__(self, entity_manager=None):
        self.entity_manager = entity_manager

    def update(self):
        pass


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
    def update(self, time):
        em = self.entity_manager
        for entity in em.get_entities_by_component_class('Display'):
            render = em.get_component('Display', entity)
            position = em.get_component('Position', entity)

            maxx = render.view.get_maxx()
            maxy = render.view.get_maxy()
            if render.y >= maxy:
                render.y = 0
                position.y = 0
            if render.y < 0:
                render.y = 0
                position.y = 0
            if render.x >= maxx:
                render.x = 0
                position.x = 0
            if render.x < 0:
                render.x = 0
                position.x = 0

            render.view.draw(render, time)


class InputSystem(System):
    def update(self, time):
        em = self.entity_manager

        for entity in em.get_entities_by_component_class('Input'):
            input = em.get_component('Input', entity)
            velocity = em.get_component('Velocity', entity)
            display = em.get_component('Display', entity)

            if not velocity:
                continue

            try:
                key = input.input.get_key()
            except:
                entity.fsm.change_state('stand')
                return

            entity.fsm.change_state('walk')
            if key == input.input.key_up():
                velocity.velocity_y = display.view.get_up_direction()
            elif key == input.input.key_down():
                velocity.velocity_y = display.view.get_down_direction()
            elif key == input.input.key_right():
                velocity.velocity_x = display.view.get_right_direction()
            elif key == input.input.key_left():
                velocity.velocity_x = display.view.get_left_direction()


class CollisionSystem(System):
    def update(self, time):
        em = self.entity_manager

        for entity in em.get_entities_by_component_class('Velocity'):
            velocity = em.get_component('Velocity', entity)
            position = em.get_component('Position', entity)

            for ent in em.get_entities_by_component_class('Position'):
                if ent == entity:
                    continue

                ent_position = em.get_component('Position', ent)

                if position.x + 1 + velocity.velocity_x == ent_position.x\
                        and position.y + velocity.velocity_y == ent_position.y:
                    velocity.velocity_x = 0
                    velocity.velocity_y = 0
