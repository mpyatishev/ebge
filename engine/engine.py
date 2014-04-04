# -*- coding: utf-8 -*-


class Engine:
    def __init__(self):
        self.systems = {}
        self.entities = []

    def add_system(self, system, priority):
        if priority not in self.systems:
            self.systems[priority] = []
        self.systems[priority].append(system)

    def update(self, time):
        for priority in self.systems:
            for system in self.systems[priority]:
                system.update(time)

    def add_entity(self, entity):
        self.enities.append(entity)
