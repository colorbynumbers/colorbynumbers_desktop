# Created by Lionel Kornberger at 2019-05-28

import numpy as np

from Surface.SmallSurfaceRemoval import SmallSurfaceRemoval


class RecursiveSurfaceHandling(SmallSurfaceRemoval):

    last_label = -1
    pixel_count = 0
    last_visited_x = -1
    adjacent_color = 0
    own_y = 0
    counted_pixel_coordinates = [None] * 100


    def remove_surface_area(self, labels_2d):

        for x, y in counted_pixel_coordinates[:pixel_count]:
            labels_2d[y][x] = adjacent_color
        return labels_2d


    def remove_small_areas(self, labels, width, height, min_surface, n_colors):
        global last_visited_x
        global pixel_count
        global counted_pixel_coordinates
        global own_y
        labels_2d = np.reshape(labels, (width, height))

        for y in range(labels_2d.shape[0]):
            last_visited_x = -1
            last_label = -1
            pixel_count = 0
            own_y = y
            for x in range(labels_2d.shape[1]):

                if x < last_visited_x or last_label == labels_2d[y][x]:
                    continue
                counted_pixel_coordinates = [None] * 100
                pixel_count = 1
                counted_pixel_coordinates[0] = tuple((x,y))
                self.get_surface_area(x_coordinate=x, y_coordinate=y, own_label=labels_2d[y][x], labels_2d=labels_2d,
                                 min_surface=min_surface)

                if pixel_count < min_surface:
                    labels_2d = self.remove_surface_area(labels_2d)

                else:
                    pass

        labels = labels_2d.flatten()
        return labels

    def get_surface_area(self, x_coordinate, y_coordinate, own_label, labels_2d, min_surface):
        global pixel_count
        global last_label
        global last_visited_x
        global adjacent_color
        global counted_pixel_coordinates

        last_label = own_label

        if pixel_count == min_surface:
            return

        if x_coordinate < (labels_2d.shape[1] - 1): # go right
            self.count_pixel(x_coordinate, y_coordinate, x_coordinate + 1, y_coordinate, own_label, labels_2d, min_surface)

        if y_coordinate > 0:  # go up

            self.count_pixel(x_coordinate, y_coordinate, x_coordinate, y_coordinate - 1, own_label, labels_2d, min_surface)

        if y_coordinate > 0 and x_coordinate < labels_2d.shape[1] - 1: # go up and right

            self.count_pixel(x_coordinate, y_coordinate, x_coordinate + 1, y_coordinate - 1, own_label, labels_2d, min_surface)

        if x_coordinate > 0: # go left
            self.count_pixel(x_coordinate, y_coordinate, x_coordinate - 1, y_coordinate, own_label, labels_2d, min_surface)

        if x_coordinate > 0 and y_coordinate > 0: # go up and left
            self.count_pixel(x_coordinate, y_coordinate, x_coordinate - 1, y_coordinate - 1, own_label, labels_2d, min_surface)

        if y_coordinate < (labels_2d.shape[0] - 1): # go down
            self.count_pixel(x_coordinate, y_coordinate, x_coordinate, y_coordinate + 1, own_label, labels_2d, min_surface)

        if y_coordinate < (labels_2d.shape[0] - 1) and x_coordinate < (labels_2d.shape[1] - 1): # go down and right
            self.count_pixel(x_coordinate, y_coordinate, x_coordinate + 1, y_coordinate + 1, own_label, labels_2d, min_surface)


    def count_pixel(self, x, y, new_x, new_y, own_label, labels_2d, min_surface):
        global pixel_count
        global adjacent_color
        global counted_pixel_coordinates
        global last_visited_x

        if pixel_count >= min_surface or self.is_already_visited(new_x, new_y):
            return
        elif np.equal(labels_2d[y][x], labels_2d[new_y][new_x]) and labels_2d[new_y][new_x] == own_label:
            if x > last_visited_x and own_y == new_y:
                last_visited_x = x
            counted_pixel_coordinates[pixel_count] = (new_x, new_y)
            pixel_count += 1
            self.get_surface_area(new_x, new_y, own_label, labels_2d, min_surface)
        elif own_label != labels_2d[new_y][new_x]:
            adjacent_color = labels_2d[new_y][new_x]


    def is_already_visited(self, x_coordinate, y_coordinate):
        return tuple((x_coordinate, y_coordinate)) in counted_pixel_coordinates