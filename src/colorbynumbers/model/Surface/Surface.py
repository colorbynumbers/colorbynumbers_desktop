# Created by Lionel Kornberger at 2019-05-28


def distance(x, coordinate):
    return (coordinate[1] - x[1]) ** 2 + (coordinate[0] - x[0]) ** 2


class Surface():
    class Neighbour:

        def __init__(self, neighbour_label=-1, index=(-1, -1), neighbour_index=-1):
            self.neighbour_label = neighbour_label
            self.index = index
            self.row = index[0]
            self.neighbour_index = neighbour_index

    surface_set = {}
    neighbour = Neighbour(-1, (-1, -1), -1)

    def __init__(self, *args, **kwargs):
        if args:
            self.surface_set = {*args}

        if kwargs:
            self.neighbour = kwargs.get('neighbour')

    def add(self, tuple):
        self.surface_set.add(tuple)

    def compute_center(self):
        sum_tuple = tuple(map(sum, zip(*self.surface_set)))
        return self.find_closest_to_in_set(
            (int(sum_tuple[0] / self.get_surface_size()), int(sum_tuple[1] / self.get_surface_size())))

    def find_closest_to_in_set(self, coordinate):
        nearest = min(self.surface_set, key=lambda x: distance(x, coordinate))
        return nearest

    def contains_coordinate(self, index):
        return not self.surface_set.isdisjoint({index})

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

    def set_center(self, tuple):
        self.center = tuple

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
