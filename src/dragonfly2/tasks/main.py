import logging
from abc import ABCMeta, abstractmethod


LOG = logging.getLogger(__name__)
RIG_TASKS = {}


def register(cls):
    RIG_TASKS[cls.config()['title']] = cls
    return cls


class RigTask(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.logger = logging.getLogger()
        self.prop_context = {}

    @property
    def props(self):
        return self.prop_context

    @staticmethod
    @abstractmethod
    def config():
        return {}

    def set_prop_defaults(self):
        self.prop_context = {}
        for prop in self.config()['props']:
            self.prop_context[prop['name']] = prop.get('default', None)

    def set_prop_values(self, ctx):
        for prop in self.config()['props']:
            self.prop_context[prop['name']] = ctx[prop['name']]

    def override_form(self, form):
        pass

    @abstractmethod
    def run(self, ctx):
        raise NotImplementedError
