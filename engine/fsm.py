# -*- coding: utf-8 -*-


class EntityState:
    pass


class StateMachine:
    def __init__(self, entity):
        self.entity = entity
        self.states = {}
        self.current_state = None

    def create_state(self, name):
        state = EntityState()
        self.states[name] = state
        return state

    def add_state(self, name, state):
        self.states[name] = state

    def change_state(self, name):
        if name not in self.states:
            raise Exception('No such %s state' % name)

        new_state = self.states[name]

        if new_state == self.current_state:
            return

        self.current_state = new_state
