# Created by Lionel Kornberger at 2019-06-14

import abc


class SmallSurfaceRemoval(abc.ABC):
    @abc.abstractmethod
    def remove_small_areas(self, labels, width, height, min_surface):
        pass
