import logging

LOG = logging.getLogger()


class BuildQueue(object):
    def __init__(self):
        self._tasks = []

    def add_component(self, component):
        self._tasks.append(component)

    def insert_component(self, index, component):
        self._tasks.insert(index, component)

    def move_up_component(self, index):
        component = self._tasks.pop(index)
        self._tasks.insert(index - 1, component)

    def move_down_component(self, index):
        component = self._tasks.pop(index)
        if index + 1 > len(self._tasks):
            index = 0
        else:
            index += 1
        self._tasks.insert(index, component)

    def remove_component(self, index):
        component = self._tasks.pop(index)
        return component

    def run(self):
        for item in self._tasks:
            try:
                item.run()
            except:
                LOG.exception('Component failed to run: {0}'.format(item.name))
