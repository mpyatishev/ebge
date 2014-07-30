# -*- coding: utf-8 -*-


def get_class_name(cls):
    if isinstance(cls, type):
        return cls.__name__
    return cls.__class__.__name__
