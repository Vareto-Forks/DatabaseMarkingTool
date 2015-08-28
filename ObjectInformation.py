__author__ = 'Amin'

import math

import cv2


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y


class ObjectInformation:
    def __init__(self):
        self.centre = Point()
        self.width = 0
        self.height = 0

        self.selected = False
        self.point_of_selection = Point()

        self.point_top_left = Point()
        self.point_bottom_right = Point()
        self._update_based_on_points()

        self.type = "type"
        #self.description = "person"

    def init(self, x1, y1, x2, y2):
        self.point_top_left.update(x1, y1)
        self.point_bottom_right.update(x2, y2)
        self.type = "temporary"
        self._update_based_on_points()

    def resize(self, x2, y2):
        self.point_bottom_right.update(x2, y2)
        self._update_based_on_points()

    def increase_size(self, top=0, down=0, left=0, right=0):
        if top != 0:
            self.point_top_left.y += top
        elif down != 0:
            self.point_bottom_right.y += down
        elif left != 0:
            self.point_top_left.x += left
        elif right != 0:
            self.point_bottom_right.x += right
        self._update_based_on_points()

    def finish(self, x2, y2):
        self.point_bottom_right.update(x2, y2)
        self.type = "person"
        self._update_based_on_points()

    def change_type_to_person(self):
        self.type = "person"

    def change_type_to_car(self):
        self.type = "car"

    def move(self, dx, dy):
        x_centre = self.centre.x + dx
        y_centre = self.centre.y + dy
        self.centre.update(x_centre, y_centre)
        self._update_base_on_centre_and_size()

    def _update_based_on_points(self):
        x1 = self.point_top_left.x
        x2 = self.point_bottom_right.x
        y1 = self.point_top_left.y
        y2 = self.point_bottom_right.y

        self.centre.update((x1 + x2)/2.0, (y1 + y2)/2.0)

        self.width = abs(x1-x2)
        self.height = abs(y1-y2)

    def _update_base_on_centre_and_size(self):
        x1 = int(self.centre.x - math.floor(self.width/2))
        x2 = int(self.centre.x + math.floor(self.width/2))
        y1 = int(self.centre.y - math.floor(self.height/2))
        y2 = int(self.centre.y + math.floor(self.height/2))

        self.point_top_left.update(x1, y1)
        self.point_bottom_right.update(x2, y2)

    def select(self, x, y):
        self.point_of_selection.update(x, y)
        self.selected = True

    # unselect is not in a dictionary, delesect is, another option in uncheck
    # http://english.stackexchange.com/questions/18465/unselect-or-deselect
    def unselect(self):
        self.selected = False

    def check_if_inside(self, x, y):
        x1 = self.point_top_left.x
        x2 = self.point_bottom_right.x
        y1 = self.point_top_left.y
        y2 = self.point_bottom_right.y

        result_x = False

        if x1 > x2:
            if x2 <= x <= x1:
                result_x = True
        else:
            if x1 <= x <= x2:
                result_x = True

        result_y = False

        if y1 > y2:
            if y2 <= y <= y1:
                result_y = True
        else:
            if y1 <= y <= y2:
                result_y = True

        result = False
        if result_x and result_y:
            result = True

        return result

    def __choose_colour_and_width(self):
        colour = (100, 100, 100)
        width = 2

        if self.selected:
            colour = (0, 255, 0)
            width = 3
        elif self.type == "temporary":
            colour = (0, 100, 255)
            width = 2
        elif self.type == "person":
            colour = (0, 0, 255)
            width = 2
        elif self.type == "car":
            colour = (255, 0, 0)
            width = 2

        return colour, width

    def draw(self, img, font):

        colour, width = self.__choose_colour_and_width()

        cv2.putText(img, self.type, self.point_top_left.to_tuple(), font, 1, colour, 1)
        cv2.rectangle(img, self.point_top_left.to_tuple(), self.point_bottom_right.to_tuple(), colour, width)

