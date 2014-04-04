# -*- coding: utf-8 -*-


from engine.system import System


class MovementSystem(System):
    def update(self, time):
        component_class = 'Position'
        em = self.entity_manager
        for entity in em.get_entities_by_component_class(component_class):
            component = em.get_component(component_class, entity)
            component.x += 1 * time

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

            if component.y >= self.maxyx[0]:
                component.y = 1
            if component.x >= self.maxyx[1]:
                component.x = 1

            component.view.draw(component)
