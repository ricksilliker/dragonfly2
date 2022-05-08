import os
import logging
import yaml
from abc import ABCMeta, abstractmethod


LOG = logging.getLogger(__name__)
RIG_TASKS = []


def load_available_tasks():
    # Clear any tasks there were previously configured, and start fresh.
    global RIG_TASKS
    RIG_TASKS = []

    # Load the default tasks that come with dragonfly already.
    load_tasks_from_path(os.path.join(os.path.dirname(__file__), 'default_tasks'))

    # Load any user tasks from DRAGONFLY_TASK_PATHS env var.
    config_paths = os.environ.get('DRAGONFLY_TASK_PATHS', None)
    if config_paths is not None:
        config_paths = config_paths.split(os.pathsep)
        for p in config_paths:
            load_tasks_from_path(p)


def load_tasks_from_path(directory):
    for item in os.listdir(directory):
        if item.endswith('.task'):
            new_task = load_task(os.path.join(directory, item))
            if new_task is not None:
                RIG_TASKS.append(new_task)


def load_task(directory):
    config_file = os.path.join(directory, 'config.yaml')
    if not os.path.isfile(config_file):
        LOG.exception('Config file missing for task {0}'.format(directory))
        return

    with open(config_file, 'r') as cfg:
        cfg_data = yaml.safe_load(cfg)


class RigTask(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.logger = logging.getLogger()
        self.props = []

    @property
    @abstractmethod
    def prop_config(self):
        return {}

    def override_form(self, form):
        pass

    @abstractmethod
    def run(self, ctx):
        raise NotImplementedError
