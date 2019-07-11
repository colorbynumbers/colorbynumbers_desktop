# Created by Lionel Kornberger at 2019-05-28

import numpy as np

from Surface.SmallSurfaceRemoval import SmallSurfaceRemoval
from Surface.Surface import Surface


def create_neighbour_for_surface_in_row(surface, length):
    y = surface.get_y_value()

    if y > 0:
        y = y - 1
        min_x: int = surface.min()[1]
        max_x: int = surface.max()[1]

        if min_x > 0:
            min_x = min_x - 1

        if max_x < length - 1:
            max_x = max_x + 1

        return set((y, value) for value in range(min_x, max_x + 1))

    else:
        return


def get_neighbour_surface_row_index(neighbour, surface_dict):
    for row_number, surface_list in surface_dict[neighbour.neighbour_label].items():
        for list_index, surface in enumerate(surface_list):
            if surface.contains_coordinate(neighbour.index):
                return neighbour.neighbour_label, row_number, list_index
    for label, label_list in surface_dict.items():
        for row_number_2, row in label_list.items():
            for list_index_2, surface in enumerate(row):
                if surface.contains_coordinate(neighbour.index):
                    return label, row_number_2, list_index_2


class IterativeSurfaceHandling(SmallSurfaceRemoval):
    labels_2d = np.empty(0)

    def remove_small_areas(self, labels, width, height, min_surface, n_colors):
        surface_dict = self.determine_surface(labels, width, height)
        IterativeSurfaceHandling.labels_2d, surface_center_dict = self.replace_labels_in_small_areas(
            IterativeSurfaceHandling.labels_2d, min_surface, surface_dict)

        return np.reshape(IterativeSurfaceHandling.labels_2d, width * height), surface_center_dict

    def determine_surface(self, labels, width, height):
        IterativeSurfaceHandling.labels_2d = np.reshape(labels, (width, height))

        max_label = IterativeSurfaceHandling.labels_2d.max()

        surface_dict = {}
        for i in range(0, max_label + 1):
            surface_dict[i] = {}

        surface_dict = self.group_rows(surface_dict)

        for label, label_dict in surface_dict.items():

            for row_number, row in label_dict.items():

                for index, surface in enumerate(row):
                    neighbours = create_neighbour_for_surface_in_row(surface, length=height)
                    if neighbours:
                        merge_list = []
                        if (row_number - 1) in surface_dict[label]:
                            for surface_above in surface_dict[label][(row_number - 1)]:
                                if surface_above.surface_set:
                                    if not neighbours.isdisjoint(surface_above.surface_set):
                                        merge_list.append(surface_above)

                            if merge_list:
                                assert surface.neighbour is not None
                                merged_surface = Surface(neighbour=surface.neighbour).union(surface.surface_set,
                                                                                            *merge_list)
                                surface_dict[label][row_number][index] = merged_surface

                                for old_surface in merge_list:
                                    surface_dict[label][(row_number - 1)].remove(old_surface)

        return surface_dict

    def replace_labels_in_small_areas(self, labels_2d, min_surface, surface_dict):

        surface_center_dict, surface_dict = self.merge_smaller_surfaces(surface_dict, min_surface)

        for label, label_dict in surface_dict.items():
            for row_number, row in label_dict.items():
                for surface in row:
                    for point in surface.surface_set:
                        labels_2d[point[0]][point[1]] = label

        return labels_2d, surface_center_dict

    @staticmethod
    def merge_smaller_surfaces(surface_dict, min_surface):
        surface_center_dict = {}
        not_all_surfaces_are_big_enough = True

        while not_all_surfaces_are_big_enough:
            surface_big_enough = True
            for label, label_dict in surface_dict.items():
                for key, surface_list in label_dict.items():
                    if surface_list:
                        remove_list = []
                        for surface in surface_list:
                            if surface.get_surface_size() < min_surface * 4:
                                surface_big_enough = False

                                new_label, row, index = get_neighbour_surface_row_index(surface.neighbour,
                                                                                        surface_dict)
                                surface_dict[new_label][row][index].set_set(
                                    set.union(surface_dict[new_label][row][index].surface_set,
                                              surface.surface_set))
                                surface_dict[new_label][row][index].set_merged(True)
                                remove_list.append((label, key, surface))

                        for item in remove_list:
                            surface_dict[item[0]][item[1]].remove(item[2])
                            break
            if surface_big_enough:
                for label_2, label_dict_2 in surface_dict.items():
                    for key_2, surface_list_2 in label_dict_2.items():
                        for surface_2 in surface_list_2:
                            if not surface_2.merged:
                                center = surface_2.compute_center()
                                surface_center_dict[str(center[0]) + " " + str(center[1])] = label_2
                not_all_surfaces_are_big_enough = False
        return surface_center_dict, surface_dict

    # group elements of same label in the same row that are neighbours together
    @staticmethod
    def group_rows(surface_dict):

        predecessor_label = -1
        row = -1
        index_list = -1
        own_index = (-1, 1)

        for index, label in np.ndenumerate(IterativeSurfaceHandling.labels_2d):

            if index[0] in surface_dict[label]:
                if predecessor_label == label:
                    index_list = len(surface_dict[label][index[0]]) - 1
                    row = index[0]
                    own_index = index
                    predecessor_label = label
                    surface_dict[label][index[0]][index_list].add(index)
                else:
                    surface_dict[label][index[0]].append(
                        Surface(index, neighbour=Surface.Neighbour(predecessor_label, own_index, index_list)))

                    if index_list > - 1:
                        surface_dict[predecessor_label][row][index_list].set_neighbour(label, index,
                                                                                       len(surface_dict[label][
                                                                                               index[0]]) - 1)
                    predecessor_label = label
                    index_list = len(surface_dict[label][index[0]]) - 1
                    row = index[0]
                    own_index = index

            else:
                if index[1] > 0 and predecessor_label != label:
                    surface_dict[predecessor_label][row][index_list].set_neighbour(label, index,
                                                                                   0)
                if index_list > -1 and predecessor_label != label:
                    surface_dict[label][index[0]] = [
                        Surface(index, neighbour=Surface.Neighbour(predecessor_label, own_index, index_list))]
                else:
                    surface_dict[label][index[0]] = [Surface(index)]

                predecessor_label = label
                row = index[0]
                index_list = 0
                own_index = index

        return surface_dict
