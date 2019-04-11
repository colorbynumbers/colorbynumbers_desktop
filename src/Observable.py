# Created by Lionel Kornberger at 2019-04-09
from abc import ABCMeta, abstractmethod


class Observer(object):
    """Abstract class for observers, provides notify method as
      interface for subjects."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, unix_timestamp):
        pass
