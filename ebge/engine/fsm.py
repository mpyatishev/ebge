# -*- coding: utf-8 -*-

# import copy
import logging

from ..utils import get_class_name


logger = logging.getLogger()


class EntityState:
    def __init__(self, components=None):
        if components:
            self.components = components
        else:
            self.components = {}

    def add(self, component):
        component_class = get_class_name(component)
        self.components[component_class] = component
        return self

    def remove(self, component):
        component_class = get_class_name(component)
        del self.components[component_class]
        return self

    def replace(self, one, two):
        pass

    def clone(self):
        return EntityState(self.components.copy())

    def get_components(self):
        return self.components


class StateMachine:
    def __init__(self, entity_manager, entity):
        self.entity_manager = entity_manager
        self.entity = entity
        self.states = {}
        self.current_state = None

        self.entity.set_fsm(self)

    def create_state(self, name):
        state = EntityState()
        self.states[name] = state
        return state

    def copy_state(self, src, target):
        state = self.states[src].clone()
        self.states[target] = state
        return state

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if name not in self.states:
            raise Exception('No such %s state' % name)

        new_state = self.states[name]

        if new_state == self.current_state:
            return

        if self.current_state:
            # logger.debug(self.current_state.get_components())
            for component in self.current_state.get_components().values():
                self.entity_manager.remove_component(component, self.entity)

        self.current_state = new_state

        # logger.debug(self.current_state.get_components())
        for component in self.current_state.get_components().values():
            self.entity_manager.add_component(component, self.entity)
