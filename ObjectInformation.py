__author__ = 'Amin'

import math


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
        #self.description = "object"

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
        self.type = "permanent"
        self._update_based_on_points()

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
