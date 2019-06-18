# Created by Lionel Kornberger at 2019-05-28

import numpy as np

from Surface.SmallSurfaceRemoval import SmallSurfaceRemoval


def calculate_neighbours(index, width):
    # first row
    if index[0] == 0:
        if index[1] == 0:
            return
        else:
            return {(0, index[1] - 1)}
    # first element in row
    elif index[1] == 0:
        return {(index[0] - 1, index[1]), (index[0] - 1, index[1] + 1)}
    # last element in row
    elif index[1] == width - 1:
        return {(index[0], index[1] - 1), (index[0] - 1, index[1] - 1), (index[0] - 1, index[1])}
    # in the middle
    else:
        return {(index[0], index[1] - 1), (index[0] - 1, index[1] - 1), (index[0] - 1, index[1]),
                (index[0] - 1, index[1] + 1)}


class IterativeSurfaceHandling(SmallSurfaceRemoval):

    def remove_small_areas(self, labels, width, height, min_surface, n_colors):
        self.determine_surface(labels, width, height, min_surface, n_colors)

    def determine_surface(self, labels, width, height, min_surface, n_colors):
        labels_2d = np.reshape(labels, (width, height))

        max = labels_2d.max()

        surface_dict = {}
        for i in range(0, max + 1):
            surface_dict[i] = {}

        for index, label in np.ndenumerate(labels_2d):
            neighbours = calculate_neighbours(index, width)
            set_exists = False

            if neighbours:
                merge_list = []

                if index[0] in surface_dict[label]:
                    for surface in surface_dict[label][index[0]]:
                        if not neighbours.isdisjoint(surface):
                            surface.add(tuple(index))
                            merge_list.append(surface)
                            surface_dict[label][index[0]].remove(surface)
                            set_exists = True

                if index[0] > 0:
                    if index[0] - 1 in surface_dict[label]:
                        for surface in surface_dict[label][index[0] - 1]:
                            if not neighbours.isdisjoint(surface):
                                surface.add(tuple(index))
                                merge_list.append(surface)
                                surface_dict[label][index[0] - 1].remove(surface)
                                set_exists = True

                if merge_list:
                    merged_set = set.union(*merge_list)
                    if index[0] in surface_dict[label]:
                        surface_dict[label][index[0]].append(merged_set)
                    else:
                        surface_dict[label][index[0]] = [merged_set]

                if not set_exists:
                    if index[0] in surface_dict[label]:
                        surface_dict[label][index[0]].append({tuple(index)})
                    else:
                        # create new list of sets in map (map->map->list->set(tuples))
                        surface_dict[label][index[0]] = [({tuple(index)})]

            # first element image has no neighbours
            else:
                # create new list of sets in map (map->map->list->set(tuples))
                surface_dict[label][index[0]] = [({tuple(index)})]
