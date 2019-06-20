# Created by Lionel Kornberger at 2019-05-28


class Surface():
    class Neighbour:

        def __init__(self, neighbour_label=-1, index=(-1,-1), neighbour_index=-1):
            self.neighbour_label = neighbour_label
            self.index = index
            self.row = index[0]
            self.neighbour_index = neighbour_index

    surface_set = {}
    neighbour = Neighbour(-1, (-1,-1), -1)

    def __init__(self, *args, **kwargs):
        if args:
            self.surface_set = {*args}

        if kwargs:
            self.neighbour = kwargs.get('neighbour')

    def add(self, tuple):
        self.surface_set.add(tuple)

    def min(self):
        return min(self.surface_set)

    def max(self):
        return max(self.surface_set)

    def get_set(self):
        return self.surface_set

    def get_surface_size(self):
        return len(self.surface_set)

    def set_set(self, set):
        self.surface_set = set

    def set_neighbour(self, neighbour_label, row, neighbour_index):
        self.neighbour = Surface.Neighbour(neighbour_label, row, neighbour_index)

    def get_y_value(self):
        if self.surface_set:
            return next(iter(self.surface_set))[0]

    def has_set(self):
        return len(self.surface_set) > 0

    def union(self, surface_set=None, *set_list):
        if surface_set:
            self.surface_set = set.union(surface_set, *[blubb.surface_set for blubb in set_list])
        else:
            self.surface_set = set.union(*[blubb.surface_set for blubb in set_list])
        return self
