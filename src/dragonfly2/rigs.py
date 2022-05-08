from abc import ABCMeta, abstractmethod
import logging


LOG = logging.getLogger()


class BuildBreakpoint(object):
    pass


class AbstractRig(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._build_steps = []

    @property
    def build_steps(self):
        return self._build_steps

    @abstractmethod
    def register(self):
        raise NotImplementedError

    @abstractmethod
    def initialize(self):
        raise NotImplementedError

    @abstractmethod
    def build(self):
        while True:
            try:
                job = self._build_queue.pop(0)
                if isinstance(job, BuildBreakpoint):
                    LOG.info('Breakpoint found, pausing build.')
                    return
                else:
                    job['callback']()
            except IndexError:
                LOG.info('All jobs completed.')
                return
            except:
                LOG.exception('Something went wrong during rig build.')
                return


