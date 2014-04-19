# -*- coding: utf-8 -*-


from utils import get_class_name


class Entity:
    components = None

    def __init__(self, eid, name=None):
        self.eid = eid
        self.name = name
        self.components = {}

    def add_component(self, component):
        component_class = get_class_name(component)
        self.components[component_class] = component


class EntityManager:
    def __init__(self):
        self.eid = 0
        self.entities = {}
        self.components = {}

    def create_entity(self, name=None):
        eid = self.get_new_eid()
        entity = Entity(eid, name=name)
        self.entities[eid] = entity
        return entity

    def remove_entity(self, entity):
        for components in self.components.values():
            del components[entity.eid]
        del self.entities[entity.eid]

    def get_new_eid(self):
        self.eid += 1
        return self.eid

    def add_component(self, component, entity):
        component_class = get_class_name(component)

        if component_class not in self.components:
            self.components[component_class] = {}

        self.components[component_class][entity.eid] = component

    def get_component(self, component_class, entity):
        if component_class in self.components\
                and entity.eid in self.components[component_class]:
            return self.components[component_class][entity.eid]
        return None

    def remove_component(self, component_class, entity):
        if component_class in self.components\
                and entity.eid in self.components[component_class]:
            del self.components[component_class][entity.eid]

    def get_entities_by_component_class(self, component_class):
        if component_class in self.components:
            return [e for e in self.entities.values()
                    if e.eid in self.components[component_class]]
        return []
